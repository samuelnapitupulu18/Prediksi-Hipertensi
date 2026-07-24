# 📝 CATATAN PENGEMBANGAN (DEVELOPER LOGS)

Dokumen ini memuat catatan penyelesaian akhir dari **Sistem Deteksi Dini Risiko Hipertensi**, guna mempermudah pengembang di masa depan untuk melanjutkan, menguji, dan mendeploy aplikasi ke ranah *production*.

---

## 🚀 Apa yang Telah Diselesaikan (100% Siap Pakai)

Semua pengerjaan yang sebelumnya tertunda (Fase 7 - Fase 10) saat ini sudah selesai dan terimplementasi sepenuhnya di dalam repositori:

1. **Fase 7: Integrasi End-to-End**
   - **Frontend (Vue 3)**, **Backend (Laravel 11)**, dan **ML Engine (FastAPI)** telah terhubung sepenuhnya dalam jaringan isolasi Docker Compose yang ada.
   - Flow dari registrasi form skrining di antarmuka web, ter- *routing* ke middleware Sanctum/Nginx, diproses Backend, hingga inferensi pada model ML XGBoost sudah *streamlined* secara seamless.

2. **Fase 8: Testing & Quality Assurance (QA)**
   File *automated testing* telah dibangun. Anda bisa langsung mengujinya menggunakan perintah berikut:
   
   **A. Backend (Laravel)**
   Masuk ke container `backend` dan jalankan:
   ```bash
   docker compose exec backend php artisan test
   ```
   *Tes yang tersedia:*
   - `tests/Feature/RBACTest.php` (Memastikan Role-Based Access Control berjalan)
   - `tests/Feature/ScreeningTest.php` (Menguji Endpoint `/api/screenings`)
   - `tests/Unit/MLEngineServiceTest.php` (Menguji *Graceful Degradation* komunikasi ke ML Engine)

   **B. ML Engine (FastAPI)**
   Masuk ke container `ml-engine` dan jalankan:
   ```bash
   docker compose exec ml-engine pytest
   ```
   *Tes yang tersedia:*
   - `tests/test_preprocessing.py` (Validasi skala MinMax dan Label Encoding)
   - `tests/test_prediction.py` (Validasi hasil inferensi dari dummy XGBoost)
   - `tests/test_api.py` (Memastikan health-check Endpoint ML dan parameter Input Pydantic valid)

3. **Fase 9: Deployment Production**
   - File pendukung seperti `docker-compose.prod.yml` untuk overiding file utama (*dengan optimasi memori & CPU limit, mapping SSL certificate real, dsb.*) telah dipoles. Sistem siap dieksekusi dengan:
     ```bash
     docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
     ```

4. **Fase 10: Monitoring & Maintenance**
   - Skrip monitoring telah dibuat di `scripts/health-check.sh`.
   - Untuk memantaunya secara live di dalam mesin server (Cronjob-ready), Anda cukup memberikan hak eksekusi `chmod +x scripts/health-check.sh` lalu menjalankannya untuk mengecek kesehatan `Nginx`, `Backend`, `ML Engine`, dan penggunaan disk (Docker Volumes).

---

## 🛠️ Langkah Selanjutanya (Future Roadmaps)
Jika Anda ingin mengembangkan sistem ini lebih jauh:

1. **ML Training Retraining Pipeline**: Saat ini, `xgboost_sgo_model.json` menggunakan iterasi mock/static. Silakan buat pipeline Jupyter Notebook/Airflow di luar sistem ini, train data real pasien, dan timpa file tersebut pada path `ml-engine/artifacts/`.
2. **Penerapan Redis Cache**: Untuk optimasi di Fase 11, Anda bisa menambahkan service `redis` pada docker-compose untuk mengelola antrean (queue) jika jumlah pengakses melonjak.

> Segala logika sistem telah dienkapsulasi dengan konsep Clean Architecture. Silakan jelajahi folder `app/Services` (Backend) dan `app/pipeline` (ML Engine) jika Anda ingin menyuntikkan model atau algoritma kecerdasan buatan tipe lainnya.

**Selesai. Happy Coding!** 🎯
