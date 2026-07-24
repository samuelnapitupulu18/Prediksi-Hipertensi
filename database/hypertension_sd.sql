-- ============================================================================
-- SISTEM DETEKSI DINI RISIKO HIPERTENSI (HT-Detect)
-- SKEMA DATABASE LENGKAP + DATA SEED - MySQL / phpMyAdmin
-- ============================================================================
-- File ini di-generate langsung dari database yang sedang berjalan, sesudah
-- perintah berikut dijalankan pada backend Laravel:
--
--     php artisan migrate --seed
--
-- Dengan demikian struktur tabel di sini DIJAMIN identik dengan migration di
-- backend/database/migrations, dan data seed-nya identik dengan
-- backend/database/seeders/DatabaseSeeder.php.
--
-- ISI DATA SEED
--   3  akun pengguna : super_admin, dokter, perawat (password: "password")
--   12 pasien        : NIK konsisten dengan tanggal lahir
--   12 skrining      : tersebar pada 6 bulan terakhir agar grafik tren terisi
--   12 prediksi      : nilai risiko/probabilitas adalah keluaran ASLI model
--                      XGBoost-SGO, bukan angka karangan
--   12 log aktivitas : mengisi halaman audit admin
--
-- CARA IMPOR (phpMyAdmin)
--   1. Buka phpMyAdmin
--   2. Menu Import -> pilih file ini -> Go
--   3. Database db_hipertensi dibuat otomatis oleh skrip ini
--
-- CARA IMPOR (command line)
--   mysql -h 127.0.0.1 -P 3307 -u root < hypertension_sd.sql
--
-- Dokumentasi perancangan lengkap: docs/perancangan-database.md
-- ============================================================================

CREATE DATABASE IF NOT EXISTS `db_hipertensi`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `db_hipertensi`;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- ----------------------------------------------------------------------------
-- Tabel: activity_logs
--   Jejak audit aktivitas pengguna. Kolom context_data WAJIB tersanitasi -
--   jangan pernah menyimpan PHI di dalamnya.
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `activity_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_logs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned DEFAULT NULL,
  `action` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `entity_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entity_id` bigint unsigned DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `ip_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `context_data` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `activity_logs_user_id_foreign` (`user_id`),
  CONSTRAINT `activity_logs_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `activity_logs` DISABLE KEYS */;
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (1,2,'screening.created','App\\Models\\Screening',1,'Skrining selesai dengan hasil risiko: medium','127.0.0.1','Seeder/1.0',NULL,'2026-02-05 02:30:00','2026-02-05 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (2,3,'screening.created','App\\Models\\Screening',2,'Skrining selesai dengan hasil risiko: medium','127.0.0.1','Seeder/1.0',NULL,'2026-02-19 02:30:00','2026-02-19 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (3,2,'screening.created','App\\Models\\Screening',3,'Skrining selesai dengan hasil risiko: high','127.0.0.1','Seeder/1.0',NULL,'2026-03-08 02:30:00','2026-03-08 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (4,3,'screening.created','App\\Models\\Screening',4,'Skrining selesai dengan hasil risiko: low','127.0.0.1','Seeder/1.0',NULL,'2026-03-22 02:30:00','2026-03-22 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (5,2,'screening.created','App\\Models\\Screening',5,'Skrining selesai dengan hasil risiko: high','127.0.0.1','Seeder/1.0',NULL,'2026-04-04 02:30:00','2026-04-04 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (6,3,'screening.created','App\\Models\\Screening',6,'Skrining selesai dengan hasil risiko: medium','127.0.0.1','Seeder/1.0',NULL,'2026-04-17 02:30:00','2026-04-17 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (7,2,'screening.created','App\\Models\\Screening',7,'Skrining selesai dengan hasil risiko: high','127.0.0.1','Seeder/1.0',NULL,'2026-05-07 02:30:00','2026-05-07 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (8,3,'screening.created','App\\Models\\Screening',8,'Skrining selesai dengan hasil risiko: medium','127.0.0.1','Seeder/1.0',NULL,'2026-05-20 02:30:00','2026-05-20 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (9,2,'screening.created','App\\Models\\Screening',9,'Skrining selesai dengan hasil risiko: high','127.0.0.1','Seeder/1.0',NULL,'2026-06-06 02:30:00','2026-06-06 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (10,3,'screening.created','App\\Models\\Screening',10,'Skrining selesai dengan hasil risiko: medium','127.0.0.1','Seeder/1.0',NULL,'2026-06-23 02:30:00','2026-06-23 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (11,2,'screening.created','App\\Models\\Screening',11,'Skrining selesai dengan hasil risiko: low','127.0.0.1','Seeder/1.0',NULL,'2026-07-05 02:30:00','2026-07-05 02:30:00');
INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `description`, `ip_address`, `user_agent`, `context_data`, `created_at`, `updated_at`) VALUES (12,3,'screening.created','App\\Models\\Screening',12,'Skrining selesai dengan hasil risiko: high','127.0.0.1','Seeder/1.0',NULL,'2026-07-10 02:30:00','2026-07-10 02:30:00');
/*!40000 ALTER TABLE `activity_logs` ENABLE KEYS */;

-- ----------------------------------------------------------------------------
-- Tabel: migrations
--   Catatan migrasi Laravel - JANGAN dihapus. Tabel ini membuat
--   "php artisan migrate" tahu bahwa skema sudah terpasang.
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `migrations` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `migration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `migrations` DISABLE KEYS */;
INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES (1,'2019_12_14_000001_create_personal_access_tokens_table',1);
INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES (2,'2024_01_01_000001_create_users_table',1);
INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES (3,'2024_01_01_000002_create_patients_table',1);
INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES (4,'2024_01_01_000003_create_screenings_table',1);
INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES (5,'2024_01_01_000004_create_predictions_table',1);
INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES (6,'2024_01_01_000005_create_activity_logs_table',1);
/*!40000 ALTER TABLE `migrations` ENABLE KEYS */;

-- ----------------------------------------------------------------------------
-- Tabel: patients
--   Data induk pasien. NIK 16 digit format Dukcapil - digit ke-7 s/d 12
--   adalah tanggal lahir DDMMYY (perempuan: DD + 40).
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nik` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` enum('male','female') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patients_nik_unique` (`nik`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (1,'3171011204750001','Budi Harjo','1975-04-12','male','081234567890','Jl. Merdeka No. 1, Jakarta','2026-02-05 02:30:00','2026-02-05 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (2,'3171016311820002','Siti Aminah','1982-11-23','female','081298765432','Jl. Sudirman No. 45, Bandung','2026-02-19 02:30:00','2026-02-19 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (3,'3171011502680003','Agus Setiawan','1968-02-15','male','081312341234','Jl. Thamrin No. 9, Surabaya','2026-03-08 02:30:00','2026-03-08 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (4,'3171014807900004','Rina Marlina','1990-07-08','female','085612345678','Jl. Gatot Subroto No. 22, Medan','2026-03-22 02:30:00','2026-03-22 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (5,'3171013010550005','Hendra Gunawan','1955-10-30','male','081198761234','Jl. Diponegoro No. 88, Semarang','2026-04-04 02:30:00','2026-04-04 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (6,'3171015703880006','Dewi Lestari','1988-03-17','female','081377889900','Jl. Ahmad Yani No. 12, Yogyakarta','2026-04-17 02:30:00','2026-04-17 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (7,'3171010509720007','Joko Prasetyo','1972-09-05','male','082145678901','Jl. Pemuda No. 5, Solo','2026-05-07 02:30:00','2026-05-07 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (8,'3171014212950008','Maya Sari','1995-12-02','female','085799001122','Jl. Veteran No. 30, Malang','2026-05-20 02:30:00','2026-05-20 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (9,'3171012106600009','Bambang Wijaya','1960-06-21','male','081233445566','Jl. Imam Bonjol No. 17, Denpasar','2026-06-06 02:30:00','2026-06-06 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (10,'3171015401780010','Nurul Hidayah','1978-01-14','female','085611223344','Jl. Kartini No. 63, Palembang','2026-06-23 02:30:00','2026-06-23 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (11,'3171010908850011','Ahmad Fauzi','1985-08-09','male','081455667788','Jl. Cendrawasih No. 8, Makassar','2026-07-05 02:30:00','2026-07-05 02:30:00');
INSERT INTO `patients` (`id`, `nik`, `name`, `date_of_birth`, `gender`, `phone_number`, `address`, `created_at`, `updated_at`) VALUES (12,'3171016705630012','Ratna Dewi','1963-05-27','female','082199887766','Jl. Melati No. 41, Pekanbaru','2026-07-10 02:30:00','2026-07-10 02:30:00');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;

-- ----------------------------------------------------------------------------
-- Tabel: personal_access_tokens
--   Token autentikasi Laravel Sanctum. Terisi otomatis saat pengguna login,
--   sehingga sengaja dibiarkan kosong di file ini.
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `personal_access_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal_access_tokens` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `tokenable_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tokenable_id` bigint unsigned NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `abilities` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `personal_access_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `personal_access_tokens` ENABLE KEYS */;

-- ----------------------------------------------------------------------------
-- Tabel: predictions
--   Hasil inferensi ML Engine (XGBoost + Squid Game Optimizer). Kolom JSON
--   menyimpan distribusi probabilitas dan bobot kepentingan fitur (XAI).
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `predictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `predictions` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `screening_id` bigint unsigned NOT NULL,
  `risk_level` enum('low','medium','high') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `confidence_score` double NOT NULL,
  `probability_distribution` json NOT NULL,
  `feature_importance` json NOT NULL,
  `model_version` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `inference_time_ms` double NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `predictions_screening_id_foreign` (`screening_id`),
  CONSTRAINT `predictions_screening_id_foreign` FOREIGN KEY (`screening_id`) REFERENCES `screenings` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `predictions` DISABLE KEYS */;
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (1,1,'medium',0.611,'{\"low\": 0.2944, \"high\": 0.0946, \"medium\": 0.611}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',12.5,'2026-02-05 02:30:00','2026-02-05 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (2,2,'medium',0.911,'{\"low\": 0.0411, \"high\": 0.0479, \"medium\": 0.911}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',10.2,'2026-02-19 02:30:00','2026-02-19 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (3,3,'high',0.5805,'{\"low\": 0.3302, \"high\": 0.5805, \"medium\": 0.0893}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',11.1,'2026-03-08 02:30:00','2026-03-08 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (4,4,'low',0.4618,'{\"low\": 0.4618, \"high\": 0.1733, \"medium\": 0.3649}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',9.8,'2026-03-22 02:30:00','2026-03-22 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (5,5,'high',0.5329,'{\"low\": 0.3833, \"high\": 0.5329, \"medium\": 0.0839}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',13,'2026-04-04 02:30:00','2026-04-04 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (6,6,'medium',0.9141,'{\"low\": 0.0395, \"high\": 0.0464, \"medium\": 0.9141}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',10.7,'2026-04-17 02:30:00','2026-04-17 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (7,7,'high',0.5824,'{\"low\": 0.3287, \"high\": 0.5824, \"medium\": 0.0889}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',12.1,'2026-05-07 02:30:00','2026-05-07 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (8,8,'medium',0.911,'{\"low\": 0.0411, \"high\": 0.0479, \"medium\": 0.911}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',9.4,'2026-05-20 02:30:00','2026-05-20 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (9,9,'high',0.5329,'{\"low\": 0.3833, \"high\": 0.5329, \"medium\": 0.0839}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',12.8,'2026-06-06 02:30:00','2026-06-06 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (10,10,'medium',0.6229,'{\"low\": 0.2545, \"high\": 0.1226, \"medium\": 0.6229}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',11.6,'2026-06-23 02:30:00','2026-06-23 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (11,11,'low',0.5039,'{\"low\": 0.5039, \"high\": 0.1656, \"medium\": 0.3305}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',10.9,'2026-07-05 02:30:00','2026-07-05 02:30:00');
INSERT INTO `predictions` (`id`, `screening_id`, `risk_level`, `confidence_score`, `probability_distribution`, `feature_importance`, `model_version`, `inference_time_ms`, `created_at`, `updated_at`) VALUES (12,12,'high',0.5873,'{\"low\": 0.3243, \"high\": 0.5873, \"medium\": 0.0884}','[{\"label\": \"Tekanan Darah Sistolik (TDS)\", \"feature\": \"systolic_bp\", \"importance\": 0.4352}, {\"label\": \"Tekanan Darah Diastolik (TDD)\", \"feature\": \"diastolic_bp\", \"importance\": 0.2145}, {\"label\": \"Indeks Massa Tubuh (IMT)\", \"feature\": \"bmi\", \"importance\": 0.142}, {\"label\": \"Usia\", \"feature\": \"age\", \"importance\": 0.0912}, {\"label\": \"Konsumsi Garam\", \"feature\": \"salt_consumption\", \"importance\": 0.0415}, {\"label\": \"Riwayat Keluarga\", \"feature\": \"family_history\", \"importance\": 0.031}, {\"label\": \"Status Perokok\", \"feature\": \"smoking_status\", \"importance\": 0.0212}, {\"label\": \"Konsumsi Daging Merah\", \"feature\": \"red_meat_consumption\", \"importance\": 0.0125}, {\"label\": \"Aktivitas Fisik\", \"feature\": \"physical_activity\", \"importance\": 0.0074}, {\"label\": \"Jenis Kelamin\", \"feature\": \"gender\", \"importance\": 0.0035}]','1.0.0-sgo-mock',12.3,'2026-07-10 02:30:00','2026-07-10 02:30:00');
/*!40000 ALTER TABLE `predictions` ENABLE KEYS */;

-- ----------------------------------------------------------------------------
-- Tabel: screenings
--   10 fitur klinis yang menjadi input model XGBoost-SGO.
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `screenings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `screenings` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `patient_id` bigint unsigned NOT NULL,
  `user_id` bigint unsigned NOT NULL,
  `age` int NOT NULL,
  `gender` enum('male','female') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `bmi` double NOT NULL,
  `family_history` tinyint(1) NOT NULL,
  `physical_activity` enum('low','moderate','high') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `smoking_status` tinyint(1) NOT NULL,
  `red_meat_consumption` enum('low','moderate','high') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `salt_consumption` enum('low','moderate','high') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `systolic_bp` int NOT NULL,
  `diastolic_bp` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `screenings_patient_id_foreign` (`patient_id`),
  KEY `screenings_user_id_foreign` (`user_id`),
  CONSTRAINT `screenings_patient_id_foreign` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  CONSTRAINT `screenings_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `screenings` DISABLE KEYS */;
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (1,1,2,51,'male',26.5,1,'moderate',1,'moderate','high',135,85,'2026-02-05 02:30:00','2026-02-05 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (2,2,3,43,'female',22.1,0,'high',0,'low','low',110,75,'2026-02-19 02:30:00','2026-02-19 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (3,3,2,58,'male',31.2,1,'low',1,'high','high',160,100,'2026-03-08 02:30:00','2026-03-08 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (4,4,3,36,'female',24.8,0,'moderate',0,'moderate','moderate',120,80,'2026-03-22 02:30:00','2026-03-22 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (5,5,2,70,'male',28.4,1,'low',0,'high','high',145,90,'2026-04-04 02:30:00','2026-04-04 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (6,6,3,38,'female',23.5,0,'high',0,'low','moderate',115,76,'2026-04-17 02:30:00','2026-04-17 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (7,7,2,53,'male',29.8,1,'low',1,'high','high',152,96,'2026-05-07 02:30:00','2026-05-07 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (8,8,3,30,'female',21.4,0,'high',0,'low','low',108,70,'2026-05-20 02:30:00','2026-05-20 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (9,9,2,66,'male',30.5,1,'low',0,'high','high',158,98,'2026-06-06 02:30:00','2026-06-06 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (10,10,3,48,'female',27.2,1,'moderate',0,'moderate','high',138,88,'2026-06-23 02:30:00','2026-06-23 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (11,11,2,40,'male',25.1,0,'moderate',1,'moderate','moderate',128,82,'2026-07-05 02:30:00','2026-07-05 02:30:00');
INSERT INTO `screenings` (`id`, `patient_id`, `user_id`, `age`, `gender`, `bmi`, `family_history`, `physical_activity`, `smoking_status`, `red_meat_consumption`, `salt_consumption`, `systolic_bp`, `diastolic_bp`, `created_at`, `updated_at`) VALUES (12,12,3,63,'female',29.3,1,'low',0,'high','high',150,94,'2026-07-10 02:30:00','2026-07-10 02:30:00');
/*!40000 ALTER TABLE `screenings` ENABLE KEYS */;

-- ----------------------------------------------------------------------------
-- Tabel: users
--   Akun tenaga kesehatan (role: super_admin | dokter | perawat).
--   Password seluruh akun bawaan: "password".
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'perawat',
  `remember_token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_email_unique` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `role`, `remember_token`, `created_at`, `updated_at`) VALUES (1,'Super Admin','admin@admin.com',NULL,'$2y$12$iwCTcLZh66SSQAF/8X4bl.2UfIS2GF5krnwtc31XbjklHKnqwMU9W','super_admin',NULL,'2026-07-22 19:56:00','2026-07-22 19:56:00');
INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `role`, `remember_token`, `created_at`, `updated_at`) VALUES (2,'Dr. Budi','dokter@admin.com',NULL,'$2y$12$g0m/8UtMj1Y48eVwQsNpr.jwD0uBqdSuqkd4T/8Lmnhyw47QtnEva','dokter',NULL,'2026-07-22 19:56:00','2026-07-22 19:56:00');
INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `role`, `remember_token`, `created_at`, `updated_at`) VALUES (3,'Suster Siti','perawat@admin.com',NULL,'$2y$12$3OZTC9W1bD5crzjrD43QRuveLN3JoghkQHIDT6sX44dL/jCKKBEpO','perawat',NULL,'2026-07-22 19:56:01','2026-07-22 19:56:01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


-- ============================================================================
-- AKHIR SKRIP
-- ============================================================================
