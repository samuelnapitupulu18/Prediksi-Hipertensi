# Use Case & Diagram UML — Sistem Deteksi Dini Risiko Hipertensi (HT-Detect)

> Arsitektur: **Relayer Architecture** — Frontend (Vue 3 SPA) → Backend/Relayer (Laravel 11 REST API) → ML Engine (FastAPI + XGBoost-SGO), database PostgreSQL, reverse proxy Nginx, seluruhnya berjalan lokal via Docker Compose.

---

## 1. Aktor

| Aktor | Deskripsi | Hak akses |
|---|---|---|
| **Perawat** | Tenaga kesehatan penginput data | Login, kelola pasien, skrining, lihat hasil & riwayat, dashboard, unduh PDF |
| **Dokter** | Tenaga medis pemeriksa | Sama dengan perawat (akses setara pada modul klinis) |
| **Super Admin** | Pengelola sistem | Semua di atas + kelola akun pengguna + lihat audit log |
| **ML Engine** *(sistem)* | Layanan prediksi internal (FastAPI) | Dipanggil backend, tidak diakses pengguna langsung |

---

## 2. Diagram Use Case

```mermaid
graph LR
    Perawat(["🧑‍⚕️ Perawat"])
    Dokter(["👨‍⚕️ Dokter"])
    Admin(["🛡️ Super Admin"])
    ML[["🤖 ML Engine (FastAPI)"]]

    subgraph Sistem HT-Detect
        UC1(UC-01 Login / Logout)
        UC2(UC-02 Kelola Data Pasien)
        UC3(UC-03 Melakukan Skrining Hipertensi)
        UC4(UC-04 Melihat Hasil & Interpretasi Klinis)
        UC5(UC-05 Melihat Penjelasan Model / XAI)
        UC6(UC-06 Mengunduh Laporan PDF)
        UC7(UC-07 Melihat Riwayat Skrining)
        UC8(UC-08 Melihat Dashboard Statistik)
        UC9(UC-09 Kelola Akun Pengguna)
        UC10(UC-10 Melihat Audit Log)
    end

    Perawat --> UC1
    Perawat --> UC2
    Perawat --> UC3
    Perawat --> UC4
    Perawat --> UC5
    Perawat --> UC6
    Perawat --> UC7
    Perawat --> UC8

    Dokter --> UC1
    Dokter --> UC2
    Dokter --> UC3
    Dokter --> UC4
    Dokter --> UC5
    Dokter --> UC6
    Dokter --> UC7
    Dokter --> UC8

    Admin --> UC1
    Admin --> UC9
    Admin --> UC10

    UC3 -.->|include: prediksi risiko| ML
    UC4 -.->|include| UC5
```

---

## 3. Deskripsi Use Case

| Kode | Nama | Aktor | Alur utama singkat |
|---|---|---|---|
| UC-01 | Login/Logout | Semua | Input email+password → Sanctum menerbitkan Bearer token → sesi aktif; logout mencabut token |
| UC-02 | Kelola Data Pasien | Perawat, Dokter | CRUD pasien; NIK unik; tanggal lahir & JK otomatis dari NIK |
| UC-03 | Skrining Hipertensi | Perawat, Dokter | Form 3 langkah (demografi → gaya hidup → tensi) → kirim ke backend → prediksi ML → simpan |
| UC-04 | Lihat Hasil & Interpretasi | Perawat, Dokter | Klasifikasi TD (PERKI/ACC-AHA), IMT (WHO Asia-Pasifik), faktor risiko, rekomendasi, tindak lanjut |
| UC-05 | Penjelasan Model (XAI) | Perawat, Dokter | Feature importance, confidence, distribusi probabilitas skrining terbaru |
| UC-06 | Unduh Laporan PDF | Perawat, Dokter | Render halaman hasil menjadi PDF (html2pdf) |
| UC-07 | Riwayat Skrining | Perawat, Dokter | Daftar skrining terpaginasi + detail per skrining |
| UC-08 | Dashboard Statistik | Perawat, Dokter | Total skrining, distribusi risiko, tren, 5 skrining terbaru |
| UC-09 | Kelola Akun Pengguna | Super Admin | CRUD user dengan role; dilindungi middleware `role:super_admin` |
| UC-10 | Audit Log | Super Admin | Daftar aktivitas (login, skrining dibuat, pasien diubah, dll.) |

**Prasyarat umum:** semua use case selain login membutuhkan token Sanctum yang valid (middleware `auth:sanctum`).

---

## 4. Sequence Diagram — UC-03 Skrining (Relayer Architecture)

```mermaid
sequenceDiagram
    autonumber
    actor P as Perawat/Dokter
    participant FE as Frontend (Vue SPA)
    participant NG as Nginx (:80)
    participant BE as Backend Laravel (Relayer)
    participant DB as PostgreSQL
    participant ML as ML Engine (FastAPI)

    P->>FE: Isi form skrining (3 langkah)
    Note over FE: NIK → tanggal lahir & JK otomatis<br/>BB+TB → IMT otomatis<br/>Validasi Zod per langkah
    FE->>NG: POST /api/screenings (Bearer token)
    NG->>BE: fastcgi → index.php
    BE->>BE: Validasi request (10 fitur klinis)
    BE->>DB: BEGIN TRANSACTION
    BE->>DB: firstOrCreate(patients, nik)
    BE->>DB: INSERT screenings
    BE->>ML: POST /predict {10 fitur}
    ML->>ML: Label encoding + Min-Max scaling
    ML->>ML: XGBoost predict_proba
    ML-->>BE: {risk_level, confidence, probability,<br/>feature_importance, model_version}
    BE->>DB: INSERT predictions
    BE->>DB: INSERT activity_logs (tanpa PHI)
    BE->>DB: COMMIT
    BE-->>FE: 201 {screening_id, prediction}
    FE->>NG: GET /api/screenings/{id}
    NG->>BE: relay
    BE->>DB: SELECT screening + patient + prediction
    BE-->>FE: 200 {data}
    FE-->>P: Halaman hasil: risiko, interpretasi klinis,<br/>XAI, rekomendasi, unduh PDF

    alt ML Engine gagal / timeout
        BE->>DB: ROLLBACK
        BE-->>FE: 500 pesan error
        FE-->>P: Banner error pada form
    end
```

---

## 5. Class Diagram — Model Domain Backend

```mermaid
classDiagram
    class User {
        +id: bigint
        +name: string
        +email: string
        +password: string ~hidden~
        +role: string
        +screenings() HasMany
    }

    class Patient {
        +id: bigint
        +nik: string~16~
        +name: string
        +date_of_birth: date
        +gender: enum
        +phone_number: string?
        +address: text?
        +screenings() HasMany
    }

    class Screening {
        +id: bigint
        +patient_id: bigint
        +user_id: bigint
        +age: int
        +gender: enum
        +bmi: float
        +family_history: bool
        +physical_activity: enum
        +smoking_status: bool
        +red_meat_consumption: enum
        +salt_consumption: enum
        +systolic_bp: int
        +diastolic_bp: int
        +patient() BelongsTo
        +user() BelongsTo
        +prediction() HasOne
    }

    class Prediction {
        +id: bigint
        +screening_id: bigint
        +risk_level: enum
        +confidence_score: float
        +probability_distribution: json
        +feature_importance: json
        +model_version: string
        +inference_time_ms: float
        +screening() BelongsTo
    }

    class ActivityLog {
        +id: bigint
        +user_id: bigint?
        +action: string
        +entity_type: string?
        +entity_id: bigint?
        +description: text?
        +user() BelongsTo
    }

    class MLEngineService {
        <<service>>
        +predict(features: array) array
        +healthCheck() bool
    }

    class ScreeningController {
        <<controller>>
        +index()
        +show(id)
        +store(request)
    }

    User "1" --> "0..*" Screening : menginput
    Patient "1" --> "0..*" Screening : memiliki
    Screening "1" --> "1" Prediction : menghasilkan
    User "1" --> "0..*" ActivityLog : tercatat
    ScreeningController ..> MLEngineService : memanggil
    ScreeningController ..> Screening : membuat
    ScreeningController ..> Prediction : menyimpan
```

---

## 6. Diagram Deployment (Docker Compose)

```mermaid
graph TB
    subgraph Host["💻 Laptop (Windows + Docker Desktop)"]
        Browser["🌐 Browser<br/>http://localhost"]
        subgraph Public["jaringan hyper_public_net"]
            NGINX["hyper_nginx<br/>Nginx :80"]
            FE["hyper_frontend<br/>Vite dev :5173"]
            BE["hyper_backend<br/>PHP-FPM 8.2 :9000"]
        end
        subgraph Internal["jaringan hyper_internal_net (terisolasi)"]
            ML["hyper_ml_engine<br/>FastAPI :8000"]
            PG[("hyper_postgres<br/>PostgreSQL 15 :5432")]
        end
    end

    Browser --> NGINX
    NGINX -->|"/ (SPA)"| FE
    NGINX -->|"/api, /sanctum (fastcgi)"| BE
    BE --> PG
    BE -->|"POST /predict"| ML
```

Jaringan `hyper_internal_net` bersifat *internal* — database dan ML Engine tidak dapat diakses dari luar host, hanya melalui backend (relayer).
