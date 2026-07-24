# HT-Detect — Sistem Deteksi Dini Risiko Hipertensi

Sistem penapisan risiko hipertensi berbasis web dengan model **XGBoost** yang
hyperparameternya dioptimasi memakai **Social Group Optimization (SGO)**.

> Skripsi — Samuel Alfred Richardo Napitupulu
> D4 Teknologi Rekayasa Perangkat Lunak, Politeknik Negeri Medan

---

## Menjalankan sistem

Klik kanan [`start-demo.ps1`](start-demo.ps1) → *Run with PowerShell*. Skrip akan
memeriksa prasyarat, menyiapkan basis data bila belum ada, menjalankan ketiga
layanan, lalu membuka browser.

| Layanan | Alamat | Teknologi |
|---|---|---|
| Frontend | http://localhost:5173 | Vue 3 + Vite + Tailwind |
| Backend | http://127.0.0.1:8001 | Laravel 11 (PHP 8.3) |
| ML Engine | http://127.0.0.1:8000 | FastAPI + XGBoost |
| Basis data | 127.0.0.1:3307 | MySQL |

Akun bawaan — kata sandi seluruhnya `password`:

| Peran | Email |
|---|---|
| Dokter | `dokter@admin.com` |
| Perawat | `perawat@admin.com` |
| Super Admin | `admin@admin.com` |

Petunjuk lengkap: **[docs/PANDUAN_DEMO.md](docs/PANDUAN_DEMO.md)**

---

## Struktur project

```
WEB SKRIPSI/
├── start-demo.ps1          Menjalankan seluruh sistem sekaligus
├── docker-compose.yml      Alternatif penjalanan memakai Docker
│
├── backend/                Laravel 11 — API, autentikasi, basis data
│   ├── app/Http/           Controller & middleware
│   ├── app/Services/       MLEngineService, DashboardService, ActivityLogService
│   ├── database/           Migration & seeder
│   └── routes/api.php      Definisi seluruh endpoint
│
├── frontend/               Vue 3 — antarmuka pengguna
│   └── src/
│       ├── pages/          Halaman per fitur (screening, xai, admin, dsb.)
│       ├── services/       Pembungkus pemanggilan API
│       ├── stores/         State autentikasi (Pinia)
│       └── router/         Definisi rute & penjaga akses
│
├── ml-engine/              FastAPI — inferensi & optimasi
│   ├── app/models/         Pembungkus model XGBoost
│   ├── app/pipeline/       Encoder & scaler (dipakai saat latih & inferensi)
│   ├── app/optimization/   Implementasi SGO + pembanding model
│   ├── artifacts/          Model terlatih & metadatanya
│   ├── data/               Dataset penelitian  (lihat data/README.md)
│   └── scripts/            Pelatihan model & eksperimen
│
├── database/               Skrip SQL lengkap + data seed
├── docs/                   Seluruh dokumentasi  (lihat docs/README.md)
└── arsip/                  Berkas lama yang TIDAK dipakai lagi
```

---

## Dokumentasi

| Dokumen | Isi |
|---|---|
| **[docs/PANDUAN_DEMO.md](docs/PANDUAN_DEMO.md)** | Cara menjalankan, akun, alur demonstrasi |
| **[docs/EKSPERIMEN_SGO.md](docs/EKSPERIMEN_SGO.md)** | Metodologi SGO, hasil pengukuran, **temuan penting soal dataset** |
| [ml-engine/data/README.md](ml-engine/data/README.md) | Asal-usul dan struktur dataset |
| [docs/perancangan-database.md](docs/perancangan-database.md) | Rancangan tabel |
| [docs/use-case-uml.md](docs/use-case-uml.md) | Diagram use case |
| [arsip/README.md](arsip/README.md) | Berkas lama dan alasan tidak dipakai lagi |

Indeks lengkap: **[docs/README.md](docs/README.md)**

> **Sebelum sidang, baca bagian 0 pada [docs/EKSPERIMEN_SGO.md](docs/EKSPERIMEN_SGO.md).**
> Ada temuan mengenai dataset yang perlu Anda putuskan bersama pembimbing.

---

## Melatih ulang model

```powershell
cd ml-engine
.\.venv\Scripts\python.exe scripts/train_production_model.py --iterations 15 --population 6
```

Menjalankan eksperimen pembanding tanpa antarmuka:

```powershell
.\.venv\Scripts\python.exe scripts/run_sgo_experiment.py --iterations 50 --runs 3
```

Membuktikan asal-usul nilai bawaan XGBoost:

```powershell
.\.venv\Scripts\python.exe scripts/show_xgboost_defaults.py
```

---

## Prinsip yang dipegang

Tidak ada angka pada sistem ini yang ditulis tangan. Metrik, kepentingan fitur,
hyperparameter, dan waktu eksekusi seluruhnya merupakan hasil perhitungan yang
dapat diulang. Berkas dari tahap awal yang dulu menghasilkan angka tidak sah
dipindahkan ke [`arsip/`](arsip/README.md) beserta penjelasan terbukanya.
