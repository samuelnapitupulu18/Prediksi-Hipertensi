# Penjelasan Sintaks Sistem Machine Learning

Dokumen ini menjelaskan **alur dan sintaks** sistem machine learning HT-Detect,
disusun agar dapat dijelaskan langsung saat sidang. Setiap bagian menyertakan
berkas sumbernya sehingga dapat ditunjuk pada saat itu juga.

---

## 1. Gambaran arsitektur — tiga lapisan

Sistem memisahkan tugas menjadi tiga lapisan yang berkomunikasi lewat HTTP
(disebut *relayer architecture*):

```
  BROWSER (Vue 3)                LARAVEL (PHP)              ML ENGINE (Python)
  ┌───────────────┐             ┌──────────────┐           ┌──────────────────┐
  │ Form skrining │──POST /api──▶│ Screening    │─POST /────▶│ FastAPI /predict │
  │               │  /screenings │ Controller   │  predict  │  + XGBoost       │
  │ Hasil skrining│◀────JSON─────│ (relay+DB)   │◀───JSON───│                  │
  └───────────────┘             └──────────────┘           └──────────────────┘
       :5173                        :8001                        :8000
```

**Mengapa dipisah?** Model machine learning ditulis dengan Python (pustaka
XGBoost, scikit-learn), sedangkan aplikasi web ditulis dengan Laravel. Keduanya
tidak bisa digabung dalam satu proses. Laravel berperan sebagai **perantara
(relay)**: menerima data dari browser, meneruskannya ke ML Engine, menerima
hasilnya, lalu menyimpannya ke basis data.

| Lapisan | Teknologi | Tugas |
|---|---|---|
| Frontend | Vue 3 + TypeScript | Form input, menampilkan hasil |
| Backend | Laravel 11 (PHP 8.3) | Autentikasi, relay ke ML Engine, simpan ke DB |
| ML Engine | FastAPI + XGBoost | Pra-pemrosesan, inferensi, penjelasan (XAI) |

---

## 2. Alur satu permintaan prediksi — langkah demi langkah

Berikut perjalanan data ketika pengguna menekan tombol "Proses" pada form
skrining. Angka pada contoh diambil dari trace sungguhan (pasien: laki-laki, 58
tahun, tensi 160/100).

### Langkah 1 — Browser mengirim data
Berkas: `frontend/src/services/screeningService.ts`

```ts
createScreening: async (data: any) => {
  const res = await api.post('/screenings', data)   // POST ke Laravel
  return res.data
}
```

Data form dikirim apa adanya ke Laravel. Tidak ada perhitungan di browser.

### Langkah 2 — Laravel memvalidasi & meneruskan
Berkas: `backend/app/Http/Controllers/Api/ScreeningController.php`

```php
$validated = $request->validate([
    'nik' => 'required|string|size:16',
    'age' => 'required|integer|min:18|max:100',
    'systolic_bp' => 'required|integer|min:70|max:250',
    // ... 10 fitur klinis
]);

// Teruskan ke ML Engine lewat MLEngineService
$predictionResult = $this->mlService->predict($mlPayload);
```

Laravel **tidak menghitung risiko sendiri** — ia hanya memvalidasi lalu
memanggil ML Engine melalui `MLEngineService`.

### Langkah 3 — MLEngineService memanggil Python
Berkas: `backend/app/Services/MLEngineService.php`

```php
$response = Http::timeout($this->timeout)
    ->retry($this->retryTimes, $this->retrySleep)
    ->post("{$this->baseUrl}/predict", $clinicalFeatures);
```

Permintaan HTTP dikirim ke `http://127.0.0.1:8000/predict`. Ada mekanisme
**retry** bila ML Engine sedang sibuk.

### Langkah 4 — FastAPI menerima & memvalidasi skema
Berkas: `ml-engine/app/schemas/request.py`

```python
class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    gender: Literal["male", "female"]
    bmi: float = Field(..., ge=10.0, le=60.0)
    systolic_bp: int = Field(..., ge=70, le=250)
    # ... total 10 fitur
```

Pydantic **menolak otomatis** data yang di luar rentang (mis. usia 200). Batas
rentang di sini **sama persis** dengan rentang scaler pada Langkah 6 — itulah
kunci konsistensi.

### Langkah 5 — Encoding: teks menjadi angka
Berkas: `ml-engine/app/pipeline/label_encoder.py`

```python
MAPPINGS = {
    "gender": {"female": 0, "male": 1},
    "physical_activity": {"low": 0, "moderate": 1, "high": 2},
    "red_meat_consumption": {"low": 0, "moderate": 1, "high": 2},
    "salt_consumption": {"low": 0, "moderate": 1, "high": 2},
}
```

Model hanya mengerti angka. `"male"` → `1`, `"high"` → `2`, dan seterusnya.
Pemetaannya **statis/hardcode** — ini disengaja untuk mencegah *data leakage*:
angka yang sama selalu dipakai baik saat melatih maupun saat memprediksi.

> Contoh: gender `male`→1, physical_activity `low`→0, salt `high`→2.

### Langkah 6 — Scaling: menyamakan skala ke rentang 0–1
Berkas: `ml-engine/app/pipeline/scaler.py`

```python
FEATURE_RANGES = {
    "age": {"min": 18.0, "max": 100.0},
    "systolic_bp": {"min": 70.0, "max": 250.0},
    # ...
}
# rumus: (nilai - min) / (max - min)
scaled = (clipped_val - f_min) / (f_max - f_min)
```

Tekanan darah (puluhan–ratusan) dan riwayat keluarga (0/1) punya skala sangat
berbeda. Min-Max Scaling menyeragamkannya ke 0–1 agar tidak ada fitur yang
mendominasi hanya karena angkanya besar.

> Contoh: age 58 → (58−18)/(100−18) = **0,4878**; systolic 160 →
> (160−70)/(250−70) = **0,5**.

### Langkah 7 — Menyusun vektor fitur dengan urutan tetap
Berkas: `ml-engine/app/pipeline/preprocessor.py`

```python
FEATURE_ORDER = [
    "age", "gender", "systolic_bp", "diastolic_bp", "bmi",
    "family_history", "physical_activity", "smoking_status",
    "red_meat_consumption", "salt_consumption",
]

ordered_features = [scaled_data[f] for f in cls.FEATURE_ORDER]
return np.array([ordered_features])   # bentuk (1, 10)
```

**Urutan fitur wajib sama** antara pelatihan dan inferensi. Bila urutan tertukar,
model akan salah membaca (mengira nilai BMI sebagai usia, dsb.). Karena itu
`FEATURE_ORDER` dipakai sebagai satu-satunya sumber urutan — baik saat melatih
maupun memprediksi.

> Hasil vektor untuk contoh:
> `[0.488, 1.0, 0.5, 0.545, 0.424, 1.0, 0.0, 1.0, 1.0, 1.0]`

### Langkah 8 — Inferensi model
Berkas: `ml-engine/app/models/xgboost_model.py`

```python
probas = self.model.predict_proba(x)[0]     # peluang tiap kelas
peluang_berisiko = float(probas[1])          # kolom "berisiko"
tingkat, sebaran = self._tingkat_dari_peluang(peluang_berisiko)
```

Model adalah **pengklasifikasi biner** (0 = tidak berisiko, 1 = berisiko),
karena label pada dataset memang dua kelas. Peluang "berisiko" lalu diterjemahkan
menjadi tiga tingkat memakai ambang:

```python
if p < 0.34:          tingkat = "low"
elif p > 0.66:        tingkat = "high"
else:                 tingkat = "medium"
```

> Untuk contoh, peluang berisiko ≈ 1,0 → **high** (keyakinan 0,9999).

### Langkah 9 — Penjelasan (XAI) & respons
Berkas: `ml-engine/app/models/xgboost_model.py` + `app/schemas/response.py`

```python
skor = self.model.get_booster().get_score(importance_type="gain")
# dinormalisasi menjadi kepentingan tiap fitur, mis. TDS 0.58, TDD 0.42
```

Kepentingan fitur **dihitung dari model** (metode *gain*), bukan ditulis tangan.
FastAPI mengembalikan JSON berisi: `risk_level`, `confidence_score`,
`probability`, `feature_importance`, `model_version`, `inference_time_ms`.

### Langkah 10 — Laravel menyimpan hasil ke basis data
Kembali ke `ScreeningController.php`:

```php
$prediction = new Prediction([
    'screening_id' => $screening->id,
    'risk_level' => $predictionResult['risk_level'],
    'probability_distribution' => $predictionResult['probability'],
    'feature_importance' => $predictionResult['feature_importance'],
    // ...
]);
$prediction->save();
DB::commit();
```

Seluruh langkah dibungkus **transaksi database** (`DB::beginTransaction()` …
`DB::commit()`), sehingga bila ada kegagalan di tengah, tidak ada data separuh
jadi yang tersimpan.

---

## 3. Bagaimana model dilatih (proses SGO)

Berkas: `ml-engine/scripts/train_production_model.py`

Pelatihan memakai **pra-pemrosesan yang sama persis** dengan inferensi — kelas
`StaticLabelEncoder` dan `StaticMinMaxScaler` yang sama dipanggil, bukan disalin.
Inilah jaminan tidak ada perbedaan perlakuan.

Urutannya:

1. **Baca dataset** `data/dataset_hipertensi.csv` (10.000 baris) dan terjemahkan
   kolomnya menjadi format form (`Laki-laki`→`male`, dst.).
2. **Bagi data**: 60% latih / 20% validasi / 20% uji (stratified).
3. **Optimasi hyperparameter dengan SGO** (`app/optimization/sgo.py`):
   ```python
   ruang = [
       SearchSpace("learning_rate", 0.01, 0.30),
       SearchSpace("max_depth", 3, 12, is_integer=True),
       SearchSpace("n_estimators", 50, 300, is_integer=True),
   ]
   # fitness = macro F1 pada data validasi
   ```
   SGO mencari kombinasi tiga hyperparameter terbaik dengan meniru perilaku
   sosial kelompok (fase *improving* dan *acquiring*).
4. **Latih model akhir** memakai hyperparameter temuan SGO.
5. **Ukur pada data uji** dan simpan model + metadata ke `artifacts/`.

### Algoritma SGO — inti sintaksnya
Berkas: `ml-engine/app/optimization/sgo.py`

```python
# Fase 1 — IMPROVING: setiap individu belajar dari yang terbaik (gbest)
candidate = self.c * population[i] + r * (gbest - population[i])

# Fase 2 — ACQUIRING: bertukar pengetahuan dengan individu lain (acak)
if fitness[i] > fitness[r_idx]:
    direction = population[i] - population[r_idx]
else:
    direction = population[r_idx] - population[i]
candidate = population[i] + r1 * direction + r2 * (gbest - population[i])
```

Sesuai rumusan asli Satapathy & Naik (2016). Tiap kandidat hanya diterima bila
nilai *fitness*-nya lebih baik (*greedy selection*).

---

## 4. Peta berkas ML dan fungsinya

| Berkas | Fungsi |
|---|---|
| `app/main.py` | Menyalakan server, memuat model ke memori satu kali |
| `app/config.py` | Lokasi berkas model & metadata |
| `app/api/routes.py` | Definisi endpoint: `/predict`, `/health`, `/model-info`, `/optimize/*` |
| `app/api/dependencies.py` | Menyediakan model yang sudah dimuat ke tiap permintaan |
| `app/schemas/request.py` | Skema & validasi data masuk (Pydantic) |
| `app/schemas/response.py` | Skema data keluar |
| `app/pipeline/label_encoder.py` | Ubah teks kategori menjadi angka |
| `app/pipeline/scaler.py` | Min-Max scaling ke rentang 0–1 |
| `app/pipeline/preprocessor.py` | Rangkai encoder + scaler + urutan fitur |
| `app/models/xgboost_model.py` | Muat model, inferensi, ambang tiga kelas, XAI |
| `app/optimization/sgo.py` | Algoritma Social Group Optimization |
| `app/optimization/benchmark.py` | Pembanding Default vs SGO (untuk halaman Uji Live) |
| `scripts/train_production_model.py` | Melatih model produksi dari dataset asli |

---

## 5. Antisipasi pertanyaan penguji

**"Mengapa perlu encoding dan scaling?"**
XGBoost hanya menerima angka, bukan teks — karena itu perlu *encoding*. *Scaling*
menyamakan skala antar fitur agar tekanan darah (ratusan) tidak mendominasi
riwayat keluarga (0/1) hanya karena angkanya besar.

**"Bagaimana memastikan pelatihan dan prediksi konsisten?"**
Keduanya memanggil **kelas yang sama persis** (`StaticLabelEncoder`,
`StaticMinMaxScaler`) dan urutan fitur yang sama (`FEATURE_ORDER`). Bukan disalin,
melainkan diimpor dari berkas yang sama — sehingga mustahil berbeda.

**"Mengapa model biner tapi tampilannya tiga tingkat?"**
Label pada dataset hanya dua kelas. Model tetap dilatih biner (jujur pada data),
lalu peluang keluarannya dibagi menjadi tiga tingkat memakai ambang 0,34 dan
0,66. Tidak ada label buatan.

**"Apa itu confidence_score?"**
Peluang kelas yang dipilih model, hasil `predict_proba`. Nilai 0,9999 berarti
model sangat yakin.

**"Mengapa ada retry di MLEngineService?"**
Bila ML Engine sedang melatih model (halaman Uji Prediksi Live), permintaan
prediksi bisa tertunda sesaat. Retry membuat sistem lebih tahan gangguan.

> **Catatan jujur mengenai dataset:** model saat ini mencapai akurasi sangat
> tinggi karena label dataset ternyata turunan dari tekanan darah. Rincian dan
> sikap yang disarankan ada pada bagian 0 [EKSPERIMEN_SGO.md](EKSPERIMEN_SGO.md).
> Pahami bagian itu sebelum sidang.

---

## 6. Membuktikan alur secara langsung

Untuk memperlihatkan seluruh transformasi di atas dengan angka nyata, jalankan
trace berikut (tanpa perlu menyalakan server):

```powershell
cd ml-engine
.\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); from app.schemas.request import PredictionRequest; from app.pipeline.preprocessor import DataPreprocessor; from app.models.xgboost_model import XGBoostModel; from app.config import settings; req=PredictionRequest(age=58,gender='male',bmi=31.2,family_history=True,physical_activity='low',smoking_status=True,red_meat_consumption='high',salt_consumption='high',systolic_bp=160,diastolic_bp=100); x=DataPreprocessor.process(req); m=XGBoostModel(); m.load(settings.MODEL_PATH,settings.MODEL_METADATA_PATH); print('vektor:', [round(float(v),3) for v in x[0]]); print('hasil:', m.predict(x))"
```

Keluarannya memperlihatkan vektor fitur akhir dan hasil prediksi, yang dapat
Anda cocokkan dengan penjelasan langkah 6–8 di atas.
