# Aksi Dasar Sistem — HT-Detect

Panduan operasional aksi-aksi dasar sistem, dari menyalakan stack sampai alur kerja tiap fitur. Cocok dipakai sebagai skrip demo/sidang.

---

## 1. Menjalankan & Mematikan Sistem

**Prasyarat:** Docker Desktop menyala.

```powershell
# dari folder root "WEB SKRIPSI"
docker compose up -d          # nyalakan semua (tambah --build jika dependensi berubah)
docker compose ps             # cek status 5 container
docker compose down           # matikan semua (data DB tetap tersimpan di volume)
```

Setelah container hidup, buka **http://localhost**.

Perintah pemeliharaan:

```powershell
docker compose exec backend php artisan migrate --seed   # migrasi + akun bawaan
docker compose logs -f backend                           # lihat log Laravel
docker compose logs -f ml-engine                         # lihat log FastAPI
```

**Akun bawaan** (password semuanya `password`):

| Email | Role |
|---|---|
| dokter@admin.com | dokter |
| perawat@admin.com | perawat |
| admin@admin.com | super_admin |

---

## 2. Aksi: Login & Logout

1. Buka http://localhost → halaman login.
2. Masukkan email & password → sistem memanggil `POST /api/login`.
3. Jika valid, Sanctum menerbitkan Bearer token yang disimpan frontend; pengguna diarahkan ke Dashboard.
4. Jika salah: pesan "Email atau kata sandi salah."
5. Logout dari menu profil → `POST /api/logout` mencabut token.

> Mode demo: jika backend tidak dapat dihubungi sama sekali, login masuk sebagai "Mode Demo (Backend Offline)" dan skrining diproses lokal berbasis aturan — hasil tetap sesuai input, ditandai `fallback-rule-based (offline)`.

---

## 3. Aksi: Skrining Hipertensi (alur inti)

Form 3 langkah di menu **Skrining**:

**Langkah 1 — Demografi & Fisik**
1. Input **NIK 16 digit** → sistem otomatis membaca **tanggal lahir, usia, dan jenis kelamin** dari digit ke-7 s/d 12 (format Dukcapil; perempuan = tanggal + 40). Tidak ada input tanggal lahir manual.
2. Input nama, berat (kg), tinggi (cm) → **IMT dihitung otomatis** dan tampil dengan satuan kg/m² + kategori WHO Asia-Pasifik.

**Langkah 2 — Gaya Hidup & Pola Makan** (semua kategori dihitung **per minggu**, mengacu PERKI)
| Faktor | Rendah/Jarang | Sedang | Tinggi/Sering |
|---|---|---|---|
| Aktivitas fisik | ≤ 1×/minggu | 2–4×/minggu | ≥ 5×/minggu |
| Daging merah | ≤ 1 porsi/minggu | 2–4 porsi/minggu | ≥ 5 porsi/minggu |
| Garam | < 35 g/minggu | 35–42 g/minggu | > 42 g/minggu |

Plus toggle riwayat keluarga & status perokok.

**Langkah 3 — Pengukuran Klinis**
Input sistolik & diastolik (mmHg) → klik **Proses**.

**Yang terjadi di belakang layar:** frontend `POST /api/screenings` → Laravel validasi → simpan pasien+skrining (transaksi) → panggil ML Engine `POST /predict` → simpan prediksi → catat audit log → kembalikan `screening_id` → frontend redirect ke halaman hasil.

---

## 4. Aksi: Membaca Hasil Skrining

Halaman hasil menampilkan berurutan:
1. **Banner hasil akhir** — Berisiko/Tidak Berisiko + confidence model.
2. **Kesimpulan klinis** — klasifikasi tekanan darah (PERKI/ACC-AHA) & IMT (kg/m², WHO Asia-Pasifik).
3. **Penjelasan klinis** + tabel referensi klasifikasi TD dengan baris pasien ditandai.
4. **Analisis 9 faktor risiko** — tiap faktor berstatus Normal / Perlu Perhatian / Risiko Tinggi.
5. **Kontribusi fitur model (XAI)** — feature importance berlabel Indonesia.
6. **Estimasi risiko kardiovaskular 10 tahun** + risiko jika tidak ditangani.
7. **Rekomendasi penanganan** & **rencana tindak lanjut**.
8. Tombol **Unduh PDF** → laporan A4 dengan nama file berisi NIK.

---

## 5. Aksi: Kelola Pasien

- **Daftar & cari**: menu Pasien → pencarian nama/NIK (`GET /api/patients?search=`).
- **Tambah/Edit**: NIK 16 digit unik; nomor telepon dikirim sebagai `phone` dan disimpan ke kolom `phone_number`.
- **Detail**: profil + seluruh riwayat skrining pasien beserta hasil prediksinya.
- **Hapus**: menghapus pasien ikut menghapus skrining & prediksinya (CASCADE).
- Dari daftar pasien bisa langsung memulai skrining baru dengan data pasien terisi otomatis.

---

## 6. Aksi: Dashboard & XAI

- **Dashboard** (`GET /api/dashboard/stats`): total skrining, total pasien, jumlah & persentase risiko tinggi/rendah, 5 skrining terbaru — semuanya angka live dari database.
- **XAI Dashboard**: menampilkan prediksi **skrining terbaru yang nyata** (gauge risiko, confidence, distribusi probabilitas, feature importance). Jika belum ada data → tombol "Mulai Skrining".

---

## 7. Aksi: Administrasi (khusus Super Admin)

- **Kelola user**: `GET/POST/PUT /api/admin/users` — dilindungi middleware `role:super_admin`; dokter/perawat mendapat 403.
- **Audit log**: `GET /api/admin/audit-logs` — jejak `user.login`, `screening.created`, `patient.updated`, dll. beserta IP & user-agent, tanpa data kesehatan pasien.

---

## 8. Ringkasan Endpoint API

| Method | Endpoint | Auth | Fungsi |
|---|---|---|---|
| POST | `/api/login` | — | Login, terbitkan token |
| POST | `/api/logout` | ✅ | Cabut token |
| GET | `/api/user` | ✅ | Profil user aktif |
| GET/POST | `/api/screenings` | ✅ | Daftar / buat skrining (+prediksi ML) |
| GET | `/api/screenings/{id}` | ✅ | Detail skrining + prediksi |
| GET/POST/PUT/DELETE | `/api/patients[/{id}]` | ✅ | CRUD pasien |
| GET | `/api/dashboard/stats` | ✅ | Statistik dashboard |
| GET | `/api/dashboard/risk-distribution` | ✅ | Distribusi risiko |
| GET | `/api/dashboard/feature-importance` | ✅ | Agregat feature importance |
| GET | `/api/dashboard/monthly-trend` | ✅ | Tren bulanan |
| GET/POST/PUT | `/api/admin/users[/{id}]` | ✅ super_admin | Kelola user |
| GET | `/api/admin/audit-logs` | ✅ super_admin | Audit log |
| GET | `/health` *(internal ML)* | — | Kesehatan ML Engine |
| POST | `/predict` *(internal ML)* | — | Inferensi XGBoost (hanya dari backend) |

---

## 9. Catatan Penting

- **Model saat ini masih mock** (`1.0.0-sgo-mock`). Sebelum sidang, ganti `ml-engine/artifacts/xgboost_sgo_model.json` + `model_metadata.json` dengan model XGBoost-SGO hasil training sebenarnya — tanpa perubahan kode.
- Sistem berjalan **100% lokal tanpa internet**; "API" yang dimaksud adalah REST API internal antar-tier (lihat `docs/use-case-uml.md`).
- Dokumen terkait: [perancangan-database.md](perancangan-database.md) · [use-case-uml.md](use-case-uml.md)
