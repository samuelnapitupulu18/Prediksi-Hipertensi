# Eksperimen XGBoost Default vs XGBoost + SGO

> **Status per 23 Juli 2026 — seluruh angka pada sistem kini hasil pengukuran.**
> Model produksi telah dilatih ulang dari dataset hipertensi asli
> (`ml-engine/scripts/train_production_model.py`), kepentingan fitur dihitung
> dari model, dan halaman Perbandingan Model membaca metadata model — bukan lagi
> angka yang dituliskan di antarmuka. Berkas lama yang memalsukan hasil
> dipindahkan ke [`arsip/`](../arsip/README.md) beserta penjelasannya.
>
> Bacalah **bagian 0** di bawah lebih dulu: ada satu temuan yang harus Anda
> putuskan bersama pembimbing sebelum sidang.

---

## 0. RINGKASAN TEMUAN YANG HARUS DIPUTUSKAN

Setelah seluruh sistem dijujurkan, muncul satu kenyataan yang tidak bisa
diperbaiki dengan kode mana pun — ini persoalan **data**, bukan pemrograman.

**Kolom `Label` pada dataset merupakan rumus pasti dari tekanan darah:**

```
Label = 0  bila (TDS < 120 DAN TDD < 80)
Label = 1  selain itu
```

Kecocokan **100% pada seluruh 10.000 baris**. Akibatnya, ketika model dilatih
apa adanya:

| Yang diukur | Hasil |
|---|---|
| Accuracy / Precision / Recall / F1 / AUC | **100%** |
| Kepentingan fitur TDS | 0.5797 |
| Kepentingan fitur TDD | 0.4203 |
| Kepentingan **8 fitur lainnya** | **0.0000 — nol persis** |
| Tingkat risiko "Sedang" pada 2.000 data uji | **0 kasus** |

Model tidak "belajar mendeteksi hipertensi"; ia hanya menghafal ambang
120/80. Usia, IMT, riwayat keluarga, merokok, aktivitas fisik, konsumsi garam,
dan konsumsi daging **tidak dipakai sama sekali**.

Bila tekanan darah dikeluarkan dari fitur, sisanya nyaris tanpa sinyal:

| Model tanpa TDS/TDD | Hasil |
|---|---|
| Menebak kelas terbanyak | 65.15% |
| XGBoost | 64.55% (di bawah tebakan) |
| Macro F1 | 45.17% |
| AUC | 58.04% (acak = 50%) |

### Artinya untuk skripsi Anda

Angka **82,45% → 93,27%** pada laporan **tidak dapat direproduksi** dari dataset
ini dengan cara apa pun yang jujur. Ada tiga arah yang bisa ditempuh — keputusan
ada pada Anda dan pembimbing:

1. **Ubah klaim di laporan** agar sesuai hasil sungguhan, lalu jadikan temuan
   "label dataset ternyata turunan tekanan darah" sebagai bagian pembahasan.
   Analisis XAI yang memperlihatkan 8 fitur bernilai nol justru menjadi bukti
   ketelitian, bukan kelemahan.
2. **Ganti atau lengkapi dataset** dengan data yang labelnya berasal dari
   diagnosis dokter, bukan turunan rumus tekanan darah. Ini satu-satunya jalan
   agar klaim "AI mendeteksi risiko" benar-benar berdiri.
3. **Ubah rumusan masalah** menjadi sistem pendukung keputusan: klasifikasi
   klinis memakai pedoman PERKI (sudah ada pada halaman hasil), sedangkan model
   berperan sebagai penapis awal. Kontribusinya berpindah dari "akurasi model"
   ke "rancang bangun sistem".

Yang jelas: apa pun yang tampil di layar sekarang adalah hasil hitungan nyata,
sehingga Anda tidak perlu khawatir tertangkap mengarang angka.

---

Dokumen ini menjelaskan apa yang sesungguhnya dijalankan pada halaman
**Uji Prediksi Live**, dan — yang paling penting — **apa yang harus Anda ketahui
tentang dataset** sebelum mempresentasikannya.

---

## 1. Apa yang berubah

Sebelumnya, "optimasi SGO" pada project ini **tidak pernah benar-benar ada**:

| Bagian | Kondisi sebelumnya | Kondisi sekarang |
|--------|--------------------|------------------|
| Algoritma SGO | Tidak ada file implementasinya | [sgo.py](../ml-engine/app/optimization/sgo.py) — improving & acquiring phase sesuai paper Satapathy & Naik (2016) |
| Hyperparameter "hasil SGO" | Angka tetap yang diketik manual | Ditemukan algoritma saat dijalankan |
| Model yang dipakai sistem | Dilatih dari `make_classification` (data acak) | Dataset hipertensi 10.000 baris |
| Angka akurasi 82.45% / 93.27% | Dikarang oleh `generator_prediksi_dinamis()` | Dihitung dari prediksi model sungguhan |
| Jumlah iterasi | Tidak ada | Diatur pengguna, 1–500 (CLI tanpa batas) |
| Kepentingan fitur | Daftar yang ditulis tangan | Dihitung dari model (metode gain) |
| Halaman Perbandingan Model | Angka tetap di berkas Vue | Membaca metadata model |

Fungsi `generator_prediksi_dinamis()` pada `simulasi_seminar.py` mengambil
jawaban benar lalu sengaja merusak sebagian tepat sebanyak yang diperlukan agar
akurasinya jatuh persis di angka target. Berkas tersebut kini sudah dipindahkan
ke [`arsip/`](../arsip/README.md) beserta penjelasan lengkapnya, dan **tidak
lagi dipakai** oleh sistem mana pun.

---

## 1b. Pembuktian nilai yang dipaparkan (permintaan penguji)

Penguji ingin membuktikan apakah ketiga nilai yang selama ini dipaparkan
benar-benar dihasilkan SGO. Halaman **Uji Prediksi Live** kini menjawab itu
secara langsung: jumlah iterasi bebas ditentukan, lalu sistem membandingkan
**tiga model** pada data uji yang sama.

Hasil nyata (iterasi 8, populasi 5, seed 42, mode tanpa tensi):

| Model | learning_rate | max_depth | n_estimators | Accuracy | Macro F1 |
|---|---|---|---|---|---|
| XGBoost Default | 0.3 | 6 | 100 | 60.80% | 51.17% |
| **Nilai yang Dipaparkan** | **0.035** | **9** | **285** | **62.40%** | 51.44% |
| XGBoost + SGO (temuan) | 0.2255 | 10 | 71 | 60.85% | **52.29%** |

**Verdikt: nilai yang dipaparkan TIDAK direproduksi oleh SGO.**

| Parameter | Dipaparkan | Ditemukan | Selisih | Toleransi | Status |
|---|---|---|---|---|---|
| learning_rate | 0.035 | 0.2255 | 0.1905 | 0.029 | tidak cocok |
| max_depth | 9 | 10 | 1 | 0.9 | tidak cocok |
| n_estimators | 285 | 71 | 214 | 25 | tidak cocok |

Uji konsistensi dengan tiga seed berbeda memperlihatkan nilainya berpindah-pindah:

| Seed | learning_rate | max_depth | n_estimators | F1 Validasi |
|---|---|---|---|---|
| 42 | 0.2255 | 10 | 71 | 53.13% |
| 49 | 0.0799 | 11 | 229 | 52.79% |
| 56 | 0.2284 | 6 | 160 | 52.16% |

### Cara membacanya saat sidang

Dua hal berbeda yang jangan tertukar:

1. **Apakah nilai 0.035 / 9 / 285 itu buruk?** Tidak. Justru model dengan nilai
   tersebut memberi **akurasi tertinggi** (62,40%), mengungguli default
   (60,80%). Jadi klaim "konfigurasi ini lebih baik daripada bawaan" **benar**
   dan dapat Anda pertahankan.
2. **Apakah nilai itu keluar dari SGO?** **Tidak terbukti.** SGO menemukan nilai
   berbeda setiap kali dijalankan, dan tak satu pun mendekati 0.035 / 9 / 285.

Penyebabnya: permukaan pencarian pada dataset ini sangat datar — beda F1 antar
konfigurasi hanya sekitar 1%, sehingga tidak ada satu titik optimum tunggal yang
bisa diklaim sebagai "hasil SGO". Ini konsekuensi langsung dari lemahnya sinyal
pada dataset (lihat bagian 3).

Sikap paling aman di hadapan penguji: sampaikan nilai tersebut sebagai
**konfigurasi terpilih yang terbukti lebih baik daripada bawaan**, bukan sebagai
"titik optimum yang ditemukan SGO", kecuali Anda menyertakan seed dan
pengaturan persis yang menghasilkannya.

---

## 2. Cara kerja eksperimen

1. Dataset dibagi **60% latih / 20% validasi / 20% uji** (stratified).
2. **XGBoost Default** dilatih dengan nilai bawaan (0.3 / 6 / 100) — lihat
   bagian 2b mengenai asal-usul angka tersebut.
3. **Model nilai yang dipaparkan** dilatih dengan 0.035 / 9 / 285 apa adanya.
4. **SGO** mencari **tiga** hyperparameter — `learning_rate` (0.01–0.30),
   `max_depth` (3–12), `n_estimators` (50–300) — dengan fitness **macro F1 pada
   data validasi**. Dibatasi tiga parameter agar pembuktiannya lurus dan mudah
   diperiksa penguji.
5. Ketiga model diukur pada **data uji yang sama**, yang tidak pernah disentuh
   selama optimasi.

Jumlah pelatihan model = `populasi + (iterasi × populasi × 2)`, karena setiap
generasi menjalankan dua fase yang masing-masing mengevaluasi seluruh populasi.

**Mengapa fitness memakai macro F1, bukan akurasi?** Kelas pada dataset timpang
(65% berisiko). Bila fitness memakai akurasi, SGO menemukan "jalan pintas":
model yang selalu menebak kelas mayoritas langsung dapat 65% tanpa belajar
apa pun. Macro F1 menghukum solusi malas seperti itu.

---

## 2b. "Dari mana angka 0.3 / 6 / 100 itu?"

Pertanyaan ini sering muncul, dan jawabannya penting: **ketiganya bukan pilihan
peneliti, melainkan nilai bawaan pustaka XGBoost.** Justru itulah sebabnya
angka tersebut dipakai sebagai pembanding — supaya perbandingannya adil, yaitu
"tanpa penyetelan sama sekali" melawan "hasil penyetelan SGO".

Sejak XGBoost 2.x, `XGBClassifier().get_params()` mengembalikan `None` untuk
ketiga parameter itu, karena penetapan nilainya diserahkan kepada inti C++ dan
baru terlihat setelah model dilatih. Karena itu sistem membacanya dari
konfigurasi booster, bukan menuliskannya di dalam kode.

Buktikan langsung di hadapan penguji:

```powershell
cd ml-engine
.\.venv\Scripts\python.exe scripts/show_xgboost_defaults.py
```

Skrip ini **tidak menuliskan satu angka pun di dalam kodenya**. Yang dicetak
adalah keluaran mentah dari pustaka: untuk setiap bukti, perintah yang
dijalankan ditampilkan lebih dulu, disusul hasil apa adanya.

Potongan keluaran pada mesin ini (XGBoost 3.2.0) — ini JSON asli yang
dikeluarkan `booster.save_config()`, bukan kalimat buatan:

```
 [mentah] gbtree_model_param — memuat jumlah pohon:
    {
      "num_parallel_tree": "1",
      "num_trees": "100"
    }

 [mentah] tree_train_param — memuat eta dan max_depth:
    {
      "eta": "0.300000012",
      "learning_rate": "0.300000012",
      "max_depth": "6",
      "min_child_weight": "1",
      "subsample": "1",
      ...
    }
```

`eta` tersimpan sebagai bilangan float32, sehingga 0.3 terbaca sebagai
0.300000012 — keduanya angka yang sama.

Bagian terakhir skrip mencetak **perintah verifikasi mandiri**: dua baris
perintah satu-baris yang dapat diketik ulang penguji tanpa perlu mempercayai
skrip ini sama sekali, lalu hasilnya dibandingkan.

Rujukan resmi:

* <https://xgboost.readthedocs.io/en/stable/parameter.html> — `eta` (alias
  `learning_rate`) bawaan **0.3**; `max_depth` bawaan **6**
* <https://xgboost.readthedocs.io/en/stable/python/python_api.html> —
  `n_estimators` pada `XGBClassifier` bawaan **100**

### "Pustakanya sendiri dari mana?"

Pertanyaan lanjutan yang sering menyusul. Rinciannya ikut tercetak pada
LANGKAH 0 skrip di atas, dibaca dari berkas metadata bawaan paket:

| Keterangan | Nilai |
|---|---|
| Nama paket | `xgboost` versi **3.2.0** |
| Lisensi | Apache-2.0 (sumber terbuka) |
| Kode sumber | <https://github.com/dmlc/xgboost> |
| Dokumentasi | <https://xgboost.readthedocs.io/en/stable/> |
| Pemelihara | Hyunsu Cho (University of Washington), Jiaming Yuan |
| Cara pemasangan | `pip` dari PyPI, sesuai `ml-engine/requirements.txt` |
| Lokasi di komputer | `ml-engine/.venv/lib/site-packages/xgboost` |

XGBoost (*eXtreme Gradient Boosting*) dikembangkan di bawah naungan **DMLC**
(Distributed Machine Learning Community). Dirintis oleh Tianqi Chen dan
dipublikasikan dalam makalah berikut — **inilah sitasi yang sebaiknya Anda
cantumkan di skripsi**:

> Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System.
> *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge
> Discovery and Data Mining*, 785–794.

Nilai bawaan parameter ditetapkan di dalam kode inti C++ pustaka tersebut, jadi
sepenuhnya di luar kendali peneliti. Paket yang terpasang berupa *wheel* siap
pakai (`py3-none-win_amd64`) — biner yang sudah dikompilasi untuk Windows.

Pada halaman Uji Prediksi Live, keterangan sumber ini ikut ditampilkan di bawah
tabel perbandingan, lengkap dengan versi pustaka yang sedang dipakai.

---

## 3. TEMUAN PENTING tentang dataset

Pada `dataset_gabungan_10000.csv`, kolom `Label` ternyata **rumus pasti dari
tekanan darah**:

```
Label = 0  bila (TDS < 120 DAN TDD < 80)
Label = 1  selain itu
```

Kecocokan aturan ini **100% pada seluruh 10.000 baris**, baik bagian Kaggle
maupun Puskesmas. Artinya label bukan hasil diagnosis independen, melainkan
turunan dari dua kolom yang juga menjadi fitur.

Konsekuensinya ada dua mode pada halaman Uji Prediksi Live:

### Mode "Dengan Tekanan Darah" (11 fitur)
Kedua model mencapai **akurasi 100%** — bukan karena modelnya hebat, tetapi
karena tinggal menghafal aturan di atas. Perbandingan Default vs SGO **hanya
bermakna pada sisi waktu**, tidak pada akurasi.

### Mode "Tanpa Tekanan Darah" (9 fitur) — mode bawaan
TDS & TDD dikeluarkan, sehingga model harus menduga risiko dari faktor gaya
hidup dan demografi saja. Ini persoalan pembelajaran yang sesungguhnya, dan
sejalan dengan tujuan **deteksi dini**: menapis risiko sebelum pasien diukur
tensinya.

Hasil pengukuran nyata (iterasi 6, populasi 5, seed 42):

| | Accuracy | Macro F1 |
|---|---|---|
| Menebak kelas terbanyak | 65.15% | — |
| XGBoost Default | 60.80% | 51.17% |
| XGBoost + SGO | 59.95% | **51.88%** |

SGO menaikkan macro F1 sekitar **+0,7%**, dan grafik konvergensi memang naik
(51,5% → 53,6% pada data validasi) seiring bertambahnya iterasi.

**Namun harus jujur:** korelasi seluruh fitur non-tensi terhadap label sangat
lemah (tertinggi hanya Usia 0,06). Kedua model bahkan berada **di bawah** angka
menebak kelas terbanyak. Dengan kata lain, **dataset ini nyaris tidak memuat
sinyal** di luar tekanan darah.

---

## 4. Konsekuensi untuk skripsi Anda

Angka **82,45% → 93,27%** yang tertulis di laporan **tidak dapat direproduksi**
dari dataset ini dengan metode apa pun yang jujur:

* Dengan tensi → 100% vs 100% (tidak ada selisih).
* Tanpa tensi → sekitar 60% vs 60% (fitur nyaris tanpa sinyal).

Bila penguji meminta Anda menjalankan ulang dan membuktikan angka tersebut,
angka itu tidak akan muncul. Ada tiga arah yang bisa Anda ambil:

1. **Perbaiki klaim di laporan** agar sesuai hasil sungguhan, dan jadikan
   temuan "label dataset merupakan turunan tekanan darah" sebagai bagian dari
   pembahasan. Ini justru menunjukkan ketelitian analisis.
2. **Ganti/lengkapi dataset** dengan data yang labelnya berasal dari diagnosis
   dokter, bukan turunan rumus tekanan darah.
3. **Ubah rumusan masalah** menjadi "deteksi dini tanpa pengukuran tensi",
   sehingga angka ±60% menjadi hasil yang wajar dan dapat dibahas apa adanya.

Keputusan ini ada di tangan Anda dan pembimbing. Yang jelas, sistemnya kini
sudah jujur: apa pun yang tampil di layar adalah hasil hitungan sungguhan.

---

## 5. Menjalankan dari terminal — bukti yang berdiri sendiri

Halaman web bagus untuk **mendemonstrasikan**, tetapi untuk **membuktikan** pada
lampiran skripsi gunakan skrip berikut. Ia tidak memerlukan backend, frontend,
maupun database — cukup Python — sehingga penguji atau pembimbing dapat
menjalankannya sendiri. **Tidak ada batas iterasi di sini.**

```powershell
cd ml-engine

# Percobaan cepat
.\.venv\Scripts\python.exe scripts/run_sgo_experiment.py --iterations 10

# Percobaan panjang, 5 pengulangan seed, hasil disimpan untuk lampiran
.\.venv\Scripts\python.exe scripts/run_sgo_experiment.py `
    --iterations 100 --population 10 --runs 5 --output hasil_eksperimen.json

# Sertakan tekanan darah sebagai fitur
.\.venv\Scripts\python.exe scripts/run_sgo_experiment.py --with-bp
```

Keluarannya berupa tabel siap salin: performa ketiga model, tabel pembuktian
per parameter, uji konsistensi antar seed, dan rincian waktu.

Pilihan yang tersedia: `--iterations`, `--population`, `--seed`, `--runs`,
`--with-bp`, `--output`, `--quiet`.

## 6. Endpoint

| Lapisan | Endpoint |
|---------|----------|
| ML Engine | `POST http://127.0.0.1:8000/optimize/compare` |
| Backend Laravel | `POST /api/optimization/compare` (perlu autentikasi) |

Isi permintaan:

```json
{
  "iterations": 10,
  "population_size": 6,
  "seed": 42,
  "verification_runs": 3,
  "include_blood_pressure": false
}
```

### Mengapa antarmuka web punya batas iterasi?

Batas pada web (iterasi ≤ 500, populasi ≤ 50, pengulangan ≤ 10) **bukan sifat
algoritma SGO**, melainkan penjagaan agar permintaan HTTP tidak melampaui waktu
tunggu. Prosesnya berjalan sinkron — browser menunggu sampai selesai — dengan
batas waktu 30 menit pada setiap lapisan (`ML_ENGINE_OPTIMIZE_TIMEOUT`, Laravel,
dan axios).

Beban kerja dapat dihitung: `populasi + (iterasi × populasi × 2)` pelatihan
model per pengulangan, masing-masing ± 0,15 detik pada mesin pengembangan.
Kotak "Perkiraan" pada halaman akan berubah kuning lalu merah bila pengaturan
Anda melampaui batas aman.

Untuk percobaan yang lebih besar dari itu, pakai skrip CLI pada bagian 5 —
di sana tidak ada batas sama sekali.
