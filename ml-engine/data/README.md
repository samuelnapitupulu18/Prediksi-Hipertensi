# Dataset Penelitian

## `dataset_hipertensi.csv`

Dataset yang dipakai untuk melatih model produksi dan menjalankan seluruh
eksperimen pada penelitian ini.

| Keterangan | Nilai |
|---|---|
| Jumlah baris | **10.000** |
| Jumlah kolom | 13 (11 fitur + `Label` + `Sumber`) |
| Berkas asal | `dataset_gabungan_10000.csv` |
| Komposisi | 7.000 baris Kaggle + 3.000 baris Puskesmas |
| Ukuran | ± 459 KB |

### Struktur kolom

| Kolom | Tipe | Nilai | Fitur model |
|---|---|---|---|
| `Usia` | bilangan bulat | 15 – 89 | ya |
| `Jenis_Kelamin` | teks | `Laki-laki`, `Perempuan` | ya |
| `TDS` | bilangan bulat | 90 – 200 | ya |
| `TDD` | bilangan bulat | 60 – 120 | ya |
| `IMT` | desimal | 15,0 – 45,0 | ya |
| `Riwayat_Keluarga` | biner | 0, 1 | ya |
| `Aktivitas_Fisik` | ordinal | 0, 1, 2 | ya |
| `Merokok` | biner | 0, 1 | ya |
| `Konsumsi_Daging` | biner | 0, 1 | ya |
| `Konsumsi_Garam` | biner | 0, 1 | ya |
| `Riwayat_Diabetes` | biner | 0, 1 | **tidak** — tidak ada padanannya pada form |
| `Label` | biner | 0 = tidak berisiko, 1 = berisiko | target |
| `Sumber` | teks | `Kaggle`, `Puskesmas` | tidak |

Distribusi target: **3.486** tidak berisiko, **6.514** berisiko (65,1% kelas
mayoritas).

---

## Peringatan penting mengenai kolom `Label`

Kolom `Label` **bukan hasil diagnosis independen**, melainkan turunan pasti dari
tekanan darah:

```
Label = 0  bila (TDS < 120 DAN TDD < 80)
Label = 1  selain itu
```

Aturan ini cocok **100% pada seluruh 10.000 baris**, baik pada bagian Kaggle
maupun Puskesmas. Akibatnya, model apa pun yang dilatih dengan menyertakan
TDS/TDD akan mencapai akurasi 100% — bukan karena kemampuan belajarnya, tetapi
karena tinggal menghafal ambang tersebut.

Bacalah **bagian 0** pada [docs/EKSPERIMEN_SGO.md](../../docs/EKSPERIMEN_SGO.md)
sebelum menarik kesimpulan apa pun dari angka akurasi.

---

## Penyesuaian saat pelatihan

Skrip [`scripts/train_production_model.py`](../scripts/train_production_model.py)
menerjemahkan kolom dataset menjadi format yang dikirim form skrining:

| Dataset | Fitur aplikasi | Penyesuaian |
|---|---|---|
| `Jenis_Kelamin` | `gender` | `Laki-laki` → `male`, `Perempuan` → `female` |
| `Aktivitas_Fisik` | `physical_activity` | 0/1/2 → `low`/`moderate`/`high` |
| `Konsumsi_Daging` | `red_meat_consumption` | 0 → `low`, 1 → `high` |
| `Konsumsi_Garam` | `salt_consumption` | 0 → `low`, 1 → `high` |
| `Riwayat_Keluarga` | `family_history` | 0/1 → boolean |
| `Merokok` | `smoking_status` | 0/1 → boolean |

Perhatikan dua baris terakhir pada tabel penyesuaian: **dataset hanya
membedakan dua tingkat** untuk konsumsi daging dan garam, sedangkan form
menyediakan tiga tingkat (rendah/sedang/tinggi). Perbedaan ini dicatat pada
metadata model agar tidak tersembunyi.

Kolom `Riwayat_Diabetes` tidak dipakai karena form skrining tidak
mengumpulkannya sebagai bidang tersendiri.

---

## Cara melatih ulang

```powershell
cd ml-engine
.\.venv\Scripts\python.exe scripts/train_production_model.py --iterations 15 --population 6
```

Keluarannya menimpa `artifacts/xgboost_sgo_model.json` dan
`artifacts/model_metadata.json`.
