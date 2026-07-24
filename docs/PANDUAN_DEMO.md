# Panduan Demonstrasi HT-Detect

Dokumen singkat untuk menjalankan dan mendemonstrasikan sistem di perangkat sendiri
(belum di-hosting).

---

## 1. Menjalankan sistem

**Cara cepat** — klik kanan `start-demo.ps1` → *Run with PowerShell*.
Skrip akan memeriksa prasyarat, membangun database bila belum ada, menjalankan
ketiga layanan di jendela terpisah, lalu membuka browser otomatis.

**Cara manual** — buka tiga terminal:

| # | Layanan | Perintah | Alamat |
|---|---------|----------|--------|
| 1 | ML Engine | `cd ml-engine` lalu `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000` | http://127.0.0.1:8000 |
| 2 | Backend | `cd backend` lalu `C:\laragon\bin\php\php-8.3.29-nts-Win32-vs16-x64\php.exe artisan serve --host=127.0.0.1 --port=8001` | http://127.0.0.1:8001 |
| 3 | Frontend | `cd frontend` lalu `npm run dev` | http://localhost:5173 |

Syarat: MySQL sudah aktif di `127.0.0.1:3307` (Laragon → Start All).

> **Penting:** backend WAJIB dijalankan dengan PHP 8.3, bukan `php` bawaan PATH
> (yang masih versi 8.0). Laravel 11 memerlukan PHP ≥ 8.2.

---

## 2. Akun untuk login

Password seluruh akun: **`password`**

| Peran | Email |
|-------|-------|
| Dokter | `dokter@admin.com` |
| Perawat | `perawat@admin.com` |
| Super Admin | `admin@admin.com` |

---

## 3. Konfigurasi yang dipakai

| Komponen | Nilai |
|----------|-------|
| Database | MySQL `127.0.0.1:3307`, database `db_hipertensi`, user `root`, tanpa password |
| Backend API | `http://127.0.0.1:8001/api` |
| ML Engine | `http://127.0.0.1:8000` |
| Frontend | `http://localhost:5173` (proxy `/api` → backend) |

Port 8080 **tidak dipakai** karena sudah ditempati layanan Laragon.

---

## 4. Isi data awal

| Tabel | Jumlah | Keterangan |
|-------|--------|------------|
| users | 3 | super_admin, dokter, perawat |
| patients | 12 | NIK 16 digit konsisten dengan tanggal lahir (format Dukcapil) |
| screenings | 12 | tersebar pada 6 bulan terakhir agar grafik tren terisi |
| predictions | 12 | risiko: 2 rendah, 5 sedang, 5 tinggi |
| activity_logs | 12 | mengisi halaman audit Super Admin |

Nilai `risk_level`, `confidence_score`, dan `probability_distribution` pada data
seed **merupakan keluaran asli model XGBoost-SGO**, diambil dengan memanggil ML
Engine untuk tiap kombinasi fitur klinis, lalu dibekukan ke dalam seeder supaya
proses seeding tidak bergantung pada ML Engine yang sedang menyala.

---

## 5. Status pengujian

Seluruh alur di bawah sudah diuji otomatis memakai browser sungguhan
(Chromium) pada 23 Juli 2026 — **tanpa satu pun error konsol maupun request
gagal**:

| Yang diuji | Hasil |
|------------|-------|
| Login dokter & super admin | lolos |
| Dashboard (statistik, tren, tabel) | lolos |
| Skrining pasien baru 3 langkah → prediksi ML | lolos |
| Halaman hasil + kesimpulan klinis | lolos |
| Riwayat skrining, daftar pasien | lolos |
| Dashboard XAI, perbandingan model | lolos |
| Refresh halaman (F5) tetap login | lolos |
| Logout | lolos |

---

## 6. Alur demonstrasi yang disarankan

1. **Login** sebagai `dokter@admin.com`.
2. **Dashboard** — tunjukkan kartu statistik, distribusi risiko, dan tren bulanan
   (terisi 6 bulan).
3. **Skrining Baru** — isi form dengan data pasien **baru** di depan penguji.
   Hasil yang muncul dihitung langsung oleh ML Engine saat itu juga; tidak ada
   nilai yang disiapkan sebelumnya.
4. **Halaman Hasil** — tunjukkan tingkat risiko, probabilitas tiap kelas, dan
   kontribusi fitur (XAI) beserta waktu inferensi sesungguhnya.
5. **Riwayat Skrining** — data yang baru diinput langsung muncul di daftar.
6. **Dashboard lagi** — angka statistik ikut bertambah, membuktikan data benar-benar
   tersimpan di database.
7. *(opsional)* Login sebagai `admin@admin.com` → **Audit Log** untuk menunjukkan
   jejak aktivitas.

---

## 7. Mengembalikan database ke kondisi awal

Bila ingin mengulang demo dari data bersih:

```powershell
cd backend
C:\laragon\bin\php\php-8.3.29-nts-Win32-vs16-x64\php.exe artisan migrate:fresh --seed
```

Atau impor ulang lampiran SQL:

```powershell
C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe -h 127.0.0.1 -P 3307 -u root < database\hypertension_sd.sql
```

File `database/hypertension_sd.sql` di-generate langsung dari database yang berjalan,
sehingga strukturnya dijamin identik dengan migrasi Laravel.

---

## 8. Catatan bila ditanya penguji

**"Kenapa ada kolom `remember_token` tapi tidak ada fitur ingat saya?"**
`remember_token` adalah kolom bawaan skeleton Laravel untuk autentikasi berbasis
session. Sistem ini memakai autentikasi *stateless* dengan bearer token Laravel
Sanctum, sehingga kolom tersebut tidak digunakan. Sesi tetap bertahan setelah
browser ditutup karena token Sanctum disimpan di `localStorage`.

**"Apakah hasil prediksinya hardcode?"**
Tidak. Halaman skrining mengirim data form ke `POST /api/screenings`, backend
meneruskannya ke ML Engine (`POST /predict`), dan hasilnya disimpan ke tabel
`predictions`. Seluruh mekanisme *fallback* yang dahulu bisa mengarang hasil saat
backend mati sudah dihapus — bila layanan bermasalah, sistem menampilkan pesan
error, bukan angka pengganti.

**"Apakah sesi login hilang kalau halaman di-refresh?"**
Tidak. Token Sanctum tersimpan di `localStorage` dan dipulihkan sebelum router
memutuskan hak akses, sehingga menekan F5 atau membuka URL langsung tetap
mempertahankan sesi.

**Halaman "Uji Prediksi Live" (`/live-comparison`)**
Halaman ini menjalankan eksperimen sungguhan. Penguji dapat menentukan sendiri
jumlah iterasi SGO, ukuran populasi, dan seed acak; saat tombol ditekan, sistem
melatih puluhan model XGBoost secara nyata lalu melaporkan akurasi, precision,
recall, F1, grafik konvergensi, serta selisih waktu antara model default dan
model hasil optimasi. Tidak ada nilai yang disiapkan sebelumnya — mengubah
jumlah iterasi akan mengubah hasilnya.

Rinciannya ada pada dokumen [EKSPERIMEN_SGO.md](EKSPERIMEN_SGO.md), termasuk
temuan penting mengenai sifat dataset yang **wajib** Anda pahami sebelum sidang.
