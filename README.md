# 🏥 Sistem Deteksi Dini Risiko Hipertensi

### Enterprise-Grade Hypertension Risk Early Detection System

> Sistem skrining klinis berbasis Explainable AI (XAI) yang memanfaatkan model XGBoost teroptimasi dengan Social Group Optimization (SGO) untuk mendeteksi risiko hipertensi secara dini. Dibangun dengan arsitektur microservices, Docker containerization, dan topologi jaringan isolasi tingkat tinggi.

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![Laravel](https://img.shields.io/badge/Laravel-11-FF2D20?logo=laravel&logoColor=white)](https://laravel.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-SGO_Optimized-blue)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📑 Daftar Isi

- [Gambaran Umum](#-gambaran-umum)
- [Fitur Utama](#-fitur-utama)
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Topologi Jaringan](#-topologi-jaringan)
- [Struktur Direktori](#-struktur-direktori)
- [Tech Stack](#-tech-stack)
- [Prasyarat](#-prasyarat)
- [Instalasi & Deployment](#-instalasi--deployment)
- [Konfigurasi Environment](#-konfigurasi-environment)
- [Alur Kerja Sistem](#-alur-kerja-sistem)
- [API Documentation](#-api-documentation)
- [ML Engine Pipeline](#-ml-engine-pipeline)
- [Frontend Components](#-frontend-components)
- [Database Schema](#-database-schema)
- [Keamanan](#-keamanan)
- [Monitoring & Logging](#-monitoring--logging)
- [Troubleshooting](#-troubleshooting)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

---

## 🚧 Status Pengembangan (Progress Checklist)
- [x] **Fase Perencanaan**: Pembuatan README, WALKTHROUGH, dan ALUR SISTEM.
- [x] **Fase 1**: Inisialisasi struktur direktori proyek.
- [x] **Fase 2**: Konfigurasi Docker & Infrastruktur (Nginx, PostgreSQL).
- [x] **Fase 3**: Pengembangan ML Engine (FastAPI, XGBoost, Preprocessing).
- [x] **Fase 4**: Pengembangan Backend (Laravel 11, Sanctum, RBAC, API).
- [x] **Fase 5**: Pengembangan Frontend (Vue 3, Tailwind, Shadcn, ECharts).
- [x] **Fase Khusus**: Refaktor UI/UX HealthTech Enterprise (Shadcn, Bento Grid, Zod).
- [ ] **Fase 6**: Integrasi End-to-End & Testing.

---

## 🌟 Gambaran Umum

**Sistem Deteksi Dini Risiko Hipertensi** adalah platform skrining klinis skala enterprise yang dirancang untuk membantu tenaga medis (Dokter dan Perawat) dalam mengidentifikasi pasien berisiko tinggi terkena hipertensi. Sistem ini menggunakan pendekatan **Explainable AI (XAI)** yang tidak hanya memberikan prediksi, tetapi juga menjelaskan **mengapa** pasien teridentifikasi berisiko melalui visualisasi **Feature Importance**.

### Mengapa Sistem Ini Dibutuhkan?

Hipertensi merupakan **silent killer** yang menyerang lebih dari 1,28 miliar orang dewasa di seluruh dunia. Deteksi dini menjadi kunci utama pencegahan komplikasi kardiovaskular. Sistem ini mengotomasi proses skrining dengan:

1. **Form skrining multi-langkah** yang intuitif untuk 11 atribut klinis pasien
2. **Prediksi real-time** menggunakan model XGBoost yang dioptimasi SGO
3. **Dashboard XAI** yang menampilkan feature importance untuk transparansi keputusan
4. **Manajemen pengguna RBAC** untuk Super Admin, Dokter, dan Perawat
5. **Audit trail** yang aman tanpa membocorkan data medis sensitif

---

## ✨ Fitur Utama

### 🩺 Fitur Klinis
| Fitur | Deskripsi |
|-------|-----------|
| **Form Skrining Multi-Langkah** | Form 4 langkah (Identitas → Riwayat Medis → Gaya Hidup → Konfirmasi) untuk 11 atribut klinis |
| **Prediksi Real-Time** | Hasil prediksi risiko hipertensi dalam < 500ms |
| **Dashboard XAI** | Visualisasi Feature Importance, Confidence Score, dan distribusi risiko |
| **Riwayat Pasien** | Tracking histori skrining per pasien dengan timeline |
| **Export Laporan** | Unduh hasil skrining dalam format PDF |

### 🔐 Fitur Keamanan
| Fitur | Deskripsi |
|-------|-----------|
| **Autentikasi Sanctum** | Cookie HTTP-Only berbasis SPA, aman dari XSS |
| **RBAC 3-Level** | Super Admin, Dokter, Perawat dengan permission granular |
| **Audit Logging** | Pencatatan aktivitas tanpa data medis sensitif |
| **Network Isolation** | Zona Publik & Internal terpisah secara logis |
| **SSL Termination** | Nginx menangani HTTPS di edge |

### 🎨 Fitur UI/UX
| Fitur | Deskripsi |
|-------|-----------|
| **Dark/Light Mode** | Toggle tema dengan transisi smooth |
| **Skeleton Loaders** | Loading state yang elegan |
| **Toast Notifications** | Feedback real-time untuk setiap aksi |
| **Responsive Design** | Mobile-first, adaptif di semua ukuran layar |
| **Animasi Transisi** | Page transition dan micro-interactions |

### 🏗️ Fitur Infrastruktur
| Fitur | Deskripsi |
|-------|-----------|
| **Docker Compose** | One-command deployment untuk seluruh stack |
| **Multi-Stage Build** | Image Docker yang optimal dan ringan |
| **Health Checks** | Endpoint `/health` di setiap service |
| **Persistent Volumes** | Data PostgreSQL persisten di Docker Volume |
| **Isolated Networks** | Segmentasi jaringan Docker |

---

## 🏛️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ZONA PUBLIK (Public Zone)                         │
│                          Network: hyper_public_net                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        NGINX REVERSE PROXY                          │  │
│  │                     Port 80 (HTTP) → 301 → 443                      │  │
│  │                     Port 443 (HTTPS/SSL Termination)                │  │
│  │                                                                     │  │
│  │  ┌─────────────────┐    ┌───────────────────────────────────────┐   │  │
│  │  │  /api/*  ──────────→ │  Backend Laravel 11 (PHP 8.2+)       │   │  │
│  │  │  /sanctum/* ───────→ │  - API Gateway & Orchestrator         │   │  │
│  │  │                 │    │  - Sanctum Auth (HTTP-Only Cookie)    │   │  │
│  │  │                 │    │  - RBAC (Admin/Dokter/Perawat)        │   │  │
│  │  │  /* (default) ────→  │  - Form Request Validation           │   │  │
│  │  │                 │    │  - API Resources                      │   │  │
│  │  │  ┌───────────┐  │    │  - Activity Logging (sanitized)      │   │  │
│  │  │  │ Vue.js 3  │  │    │  - HTTP Client → ML Engine           │   │  │
│  │  │  │ Frontend  │  │    └───────────────────────────────────────┘   │  │
│  │  │  │ (SPA)     │  │                     │                          │  │
│  │  │  └───────────┘  │                     │ HTTP (internal)          │  │
│  │  └─────────────────┘                     │                          │  │
│  └──────────────────────────────────────────┼──────────────────────────┘  │
│                                             │                             │
├─────────────────────────────────────────────┼─────────────────────────────┤
│                                             │                             │
│                          ZONA INTERNAL (Internal Zone)                    │
│                          Network: hyper_internal_net                      │
│                          ⛔ NO INTERNET ACCESS                            │
│  ┌──────────────────────────────────────────┼──────────────────────────┐  │
│  │                                          ▼                          │  │
│  │  ┌───────────────────────────────────────────────────────────────┐  │  │
│  │  │              ML ENGINE (FastAPI + Uvicorn)                    │  │  │
│  │  │              Python 3.10+ | Port 8000 (internal)             │  │  │
│  │  │                                                               │  │  │
│  │  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐  │  │  │
│  │  │  │  Pydantic   │  │ Preprocessing│  │  XGBoost Model      │  │  │  │
│  │  │  │  v2 I/O     │→ │ Pipeline     │→ │  (SGO-Optimized)    │  │  │  │
│  │  │  │  Validation │  │ - Label Enc  │  │  - LR: 0.035        │  │  │  │
│  │  │  │             │  │ - MinMax     │  │  - Max Depth: 9     │  │  │  │
│  │  │  │             │  │   (Static)   │  │  - Estimators: 285  │  │  │  │
│  │  │  └─────────────┘  └──────────────┘  └─────────────────────┘  │  │  │
│  │  └───────────────────────────────────────────────────────────────┘  │  │
│  │                                                                     │  │
│  │  ┌───────────────────────────────────────────────────────────────┐  │  │
│  │  │              POSTGRESQL 15                                    │  │  │
│  │  │              Port 5432 (internal only)                        │  │  │
│  │  │              Docker Volume: hyper_pgdata                      │  │  │
│  │  └───────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Alur Request (Request Flow)

```
Client Browser
    │
    ▼
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  NGINX  │────→│ Laravel  │────→│ FastAPI  │────→│ XGBoost  │
│  :443   │←────│ Backend  │←────│ ML Engine│←────│ Model    │
└─────────┘     └──────────┘     └──────────┘     └──────────┘
    │                │
    │                ▼
    │           ┌──────────┐
    │           │PostgreSQL│
    │           │ Database │
    │           └──────────┘
    ▼
┌─────────┐
│ Vue.js  │
│ SPA     │
└─────────┘
```

---

## 🌐 Topologi Jaringan

### Docker Networks

| Network | Tipe | Tujuan | Services |
|---------|------|--------|----------|
| `hyper_public_net` | bridge | Komunikasi zona publik | nginx, frontend, backend |
| `hyper_internal_net` | internal | Komunikasi zona terisolasi | backend, ml-engine, postgres |

### Port Mapping

| Service | Internal Port | External Port | Akses |
|---------|--------------|---------------|-------|
| Nginx | 80, 443 | 80, 443 | Publik |
| Frontend (Vite Dev) | 5173 | - | Via Nginx |
| Backend (PHP-FPM) | 9000 | - | Via Nginx |
| ML Engine (Uvicorn) | 8000 | - | Internal Only |
| PostgreSQL | 5432 | - | Internal Only |

### Aturan Isolasi

```
✅ nginx       → frontend     (hyper_public_net)
✅ nginx       → backend      (hyper_public_net)
✅ backend     → ml-engine    (hyper_internal_net)
✅ backend     → postgres     (hyper_internal_net)
✅ ml-engine   → postgres     (hyper_internal_net)  [optional]
❌ nginx       → ml-engine    (BLOCKED - different network)
❌ nginx       → postgres     (BLOCKED - different network)
❌ frontend    → ml-engine    (BLOCKED - different network)
❌ frontend    → postgres     (BLOCKED - different network)
❌ ml-engine   → internet     (BLOCKED - internal network)
❌ postgres    → internet     (BLOCKED - internal network)
```

---

## 📂 Struktur Direktori

```
hypertension-detection-system/
│
├── 📄 README.md                          # Dokumentasi utama (file ini)
├── 📄 WALKTHROUGH.md                     # Panduan walkthrough lengkap
├── 📄 docker-compose.yml                 # Orkestrasi multi-container
├── 📄 docker-compose.prod.yml            # Override untuk production
├── 📄 .env.example                       # Template environment variables
├── 📄 Makefile                           # Shortcut commands
├── 📄 LICENSE                            # Lisensi MIT
│
├── 📁 nginx/                             # Reverse Proxy Configuration
│   ├── 📄 Dockerfile                     # Nginx custom image
│   ├── 📄 nginx.conf                     # Main nginx config
│   ├── 📁 conf.d/
│   │   ├── 📄 default.conf              # Server block configuration
│   │   └── 📄 upstream.conf             # Upstream definitions
│   ├── 📁 ssl/
│   │   ├── 📄 self-signed.crt           # Self-signed cert (dev)
│   │   └── 📄 self-signed.key           # Private key (dev)
│   └── 📁 snippets/
│       ├── 📄 security-headers.conf     # Security headers
│       └── 📄 proxy-params.conf         # Proxy parameters
│
├── 📁 frontend/                          # Vue.js 3 SPA
│   ├── 📄 Dockerfile                     # Multi-stage build
│   ├── 📄 Dockerfile.dev                 # Development with HMR
│   ├── 📄 package.json
│   ├── 📄 tsconfig.json
│   ├── 📄 vite.config.ts
│   ├── 📄 tailwind.config.ts
│   ├── 📄 postcss.config.js
│   ├── 📄 components.json               # Shadcn Vue config
│   ├── 📄 index.html
│   ├── 📁 public/
│   │   ├── 📄 favicon.ico
│   │   └── 📁 assets/
│   │       └── 📄 logo.svg
│   └── 📁 src/
│       ├── 📄 main.ts                    # Entry point
│       ├── 📄 App.vue                    # Root component
│       ├── 📄 env.d.ts                   # Type declarations
│       │
│       ├── 📁 assets/
│       │   └── 📁 styles/
│       │       ├── 📄 globals.css        # Global styles + Tailwind
│       │       └── 📄 transitions.css   # Page transition animations
│       │
│       ├── 📁 components/                # Shared UI Components
│       │   ├── 📁 ui/                    # Shadcn Vue components
│       │   │   ├── 📁 button/
│       │   │   ├── 📁 card/
│       │   │   ├── 📁 dialog/
│       │   │   ├── 📁 input/
│       │   │   ├── 📁 select/
│       │   │   ├── 📁 toast/
│       │   │   ├── 📁 skeleton/
│       │   │   ├── 📁 badge/
│       │   │   ├── 📁 avatar/
│       │   │   └── 📁 dropdown-menu/
│       │   ├── 📄 AppHeader.vue          # Navigation header
│       │   ├── 📄 AppSidebar.vue         # Sidebar navigation
│       │   ├── 📄 AppFooter.vue          # Footer
│       │   ├── 📄 ThemeToggle.vue        # Dark/Light mode switch
│       │   ├── 📄 SkeletonLoader.vue     # Skeleton loading states
│       │   └── 📄 ToastNotification.vue  # Toast feedback
│       │
│       ├── 📁 composables/              # Composition API hooks
│       │   ├── 📄 useAuth.ts            # Authentication logic
│       │   ├── 📄 useTheme.ts           # Theme management
│       │   ├── 📄 useScreening.ts       # Screening form logic
│       │   └── 📄 useToast.ts           # Toast notifications
│       │
│       ├── 📁 layouts/
│       │   ├── 📄 DefaultLayout.vue     # Authenticated layout
│       │   ├── 📄 AuthLayout.vue        # Login/Register layout
│       │   └── 📄 BlankLayout.vue       # Minimal layout
│       │
│       ├── 📁 lib/
│       │   └── 📄 utils.ts              # Utility functions (cn, etc.)
│       │
│       ├── 📁 pages/                    # Route views
│       │   ├── 📁 auth/
│       │   │   ├── 📄 LoginPage.vue
│       │   │   └── 📄 ForgotPassword.vue
│       │   ├── 📁 dashboard/
│       │   │   └── 📄 DashboardPage.vue  # Main dashboard
│       │   ├── 📁 screening/
│       │   │   ├── 📄 ScreeningForm.vue   # Multi-step form
│       │   │   ├── 📄 ScreeningResult.vue # Prediction result
│       │   │   └── 📄 ScreeningHistory.vue
│       │   ├── 📁 patients/
│       │   │   ├── 📄 PatientList.vue
│       │   │   └── 📄 PatientDetail.vue
│       │   ├── 📁 xai/
│       │   │   └── 📄 XAIDashboard.vue    # Explainable AI dashboard
│       │   └── 📁 admin/
│       │       ├── 📄 UserManagement.vue
│       │       └── 📄 AuditLog.vue
│       │
│       ├── 📁 router/
│       │   ├── 📄 index.ts              # Vue Router config
│       │   └── 📄 guards.ts             # Navigation guards
│       │
│       ├── 📁 services/                 # API service layer
│       │   ├── 📄 api.ts                # Axios instance
│       │   ├── 📄 authService.ts        # Auth API calls
│       │   ├── 📄 screeningService.ts   # Screening API calls
│       │   ├── 📄 patientService.ts     # Patient API calls
│       │   └── 📄 adminService.ts       # Admin API calls
│       │
│       ├── 📁 stores/                   # Pinia Stores
│       │   ├── 📄 authStore.ts          # Auth state
│       │   ├── 📄 screeningStore.ts     # Screening state
│       │   ├── 📄 themeStore.ts         # Theme state
│       │   └── 📄 uiStore.ts            # UI state (sidebar, etc.)
│       │
│       ├── 📁 queries/                  # TanStack Vue Query
│       │   ├── 📄 useScreeningQueries.ts
│       │   ├── 📄 usePatientQueries.ts
│       │   └── 📄 useDashboardQueries.ts
│       │
│       ├── 📁 types/                    # TypeScript types
│       │   ├── 📄 auth.ts
│       │   ├── 📄 screening.ts
│       │   ├── 📄 patient.ts
│       │   └── 📄 api.ts
│       │
│       └── 📁 validations/             # Zod schemas
│           ├── 📄 authSchema.ts
│           └── 📄 screeningSchema.ts    # 11 atribut validasi
│
├── 📁 backend/                           # Laravel 11 API
│   ├── 📄 Dockerfile                     # Multi-stage build
│   ├── 📄 Dockerfile.dev                 # Development
│   ├── 📄 composer.json
│   ├── 📄 .env.example
│   ├── 📄 artisan
│   ├── 📁 app/
│   │   ├── 📁 Http/
│   │   │   ├── 📁 Controllers/
│   │   │   │   ├── 📁 Auth/
│   │   │   │   │   ├── 📄 LoginController.php
│   │   │   │   │   ├── 📄 LogoutController.php
│   │   │   │   │   └── 📄 ProfileController.php
│   │   │   │   ├── 📁 Api/
│   │   │   │   │   ├── 📄 ScreeningController.php
│   │   │   │   │   ├── 📄 PatientController.php
│   │   │   │   │   ├── 📄 DashboardController.php
│   │   │   │   │   └── 📄 UserController.php
│   │   │   │   └── 📄 HealthCheckController.php
│   │   │   ├── 📁 Middleware/
│   │   │   │   ├── 📄 RoleMiddleware.php
│   │   │   │   ├── 📄 SanitizeLogMiddleware.php
│   │   │   │   └── 📄 ForceJsonResponse.php
│   │   │   ├── 📁 Requests/
│   │   │   │   ├── 📄 StoreScreeningRequest.php
│   │   │   │   ├── 📄 StorePatientRequest.php
│   │   │   │   └── 📄 UpdateUserRequest.php
│   │   │   └── 📁 Resources/
│   │   │       ├── 📄 ScreeningResource.php
│   │   │       ├── 📄 PatientResource.php
│   │   │       ├── 📄 UserResource.php
│   │   │       └── 📄 PredictionResource.php
│   │   ├── 📁 Models/
│   │   │   ├── 📄 User.php
│   │   │   ├── 📄 Patient.php
│   │   │   ├── 📄 Screening.php
│   │   │   ├── 📄 Prediction.php
│   │   │   └── 📄 ActivityLog.php
│   │   ├── 📁 Services/
│   │   │   ├── 📄 MLEngineService.php        # HTTP Client to ML Engine
│   │   │   ├── 📄 ScreeningService.php
│   │   │   └── 📄 ActivityLogService.php
│   │   ├── 📁 Enums/
│   │   │   ├── 📄 UserRole.php               # Admin, Dokter, Perawat
│   │   │   └── 📄 RiskLevel.php              # Low, Medium, High
│   │   └── 📁 Exceptions/
│   │       ├── 📄 MLEngineException.php
│   │       └── 📄 Handler.php
│   ├── 📁 config/
│   │   ├── 📄 sanctum.php
│   │   ├── 📄 cors.php
│   │   └── 📄 services.php                   # ML Engine config
│   ├── 📁 database/
│   │   ├── 📁 migrations/
│   │   │   ├── 📄 0001_create_users_table.php
│   │   │   ├── 📄 0002_create_patients_table.php
│   │   │   ├── 📄 0003_create_screenings_table.php
│   │   │   ├── 📄 0004_create_predictions_table.php
│   │   │   └── 📄 0005_create_activity_logs_table.php
│   │   ├── 📁 seeders/
│   │   │   ├── 📄 DatabaseSeeder.php
│   │   │   ├── 📄 UserSeeder.php
│   │   │   └── 📄 RoleSeeder.php
│   │   └── 📁 factories/
│   │       ├── 📄 UserFactory.php
│   │       └── 📄 PatientFactory.php
│   ├── 📁 routes/
│   │   ├── 📄 api.php                         # API routes
│   │   └── 📄 web.php                         # Sanctum CSRF
│   └── 📁 tests/
│       ├── 📁 Feature/
│       │   ├── 📄 AuthTest.php
│       │   ├── 📄 ScreeningTest.php
│       │   └── 📄 RBACTest.php
│       └── 📁 Unit/
│           └── 📄 MLEngineServiceTest.php
│
├── 📁 ml-engine/                             # FastAPI ML Service
│   ├── 📄 Dockerfile                         # Multi-stage build
│   ├── 📄 requirements.txt
│   ├── 📄 pyproject.toml
│   ├── 📁 app/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py                        # FastAPI application
│   │   ├── 📄 config.py                      # Settings & configuration
│   │   ├── 📁 api/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 routes.py                  # API endpoints
│   │   │   └── 📄 dependencies.py            # DI dependencies
│   │   ├── 📁 core/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 exceptions.py              # Custom exceptions
│   │   │   ├── 📄 logging.py                 # Structured logging
│   │   │   └── 📄 middleware.py              # Request/Response middleware
│   │   ├── 📁 models/
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 xgboost_model.py           # Model loader & predictor
│   │   ├── 📁 pipeline/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 preprocessor.py            # Deterministic preprocessing
│   │   │   ├── 📄 label_encoder.py           # Static label encoding
│   │   │   └── 📄 scaler.py                  # Static MinMax scaling
│   │   └── 📁 schemas/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 request.py                 # Pydantic v2 input
│   │       └── 📄 response.py               # Pydantic v2 output
│   ├── 📁 artifacts/                         # ML Artifacts
│   │   ├── 📄 xgboost_sgo_model.json         # Trained model
│   │   └── 📄 model_metadata.json            # Training metadata
│   └── 📁 tests/
│       ├── 📄 __init__.py
│       ├── 📄 test_preprocessing.py
│       ├── 📄 test_prediction.py
│       └── 📄 test_api.py
│
└── 📁 docs/                                  # Documentation
    ├── 📄 architecture.md                    # Architecture deep-dive
    ├── 📄 api-reference.md                   # Full API reference
    ├── 📄 deployment-guide.md                # Production deployment
    ├── 📄 security-audit.md                  # Security considerations
    └── 📁 diagrams/
        ├── 📄 system-architecture.drawio
        ├── 📄 database-erd.drawio
        └── 📄 sequence-diagrams.drawio
```

---

## 🛠️ Tech Stack

### Frontend
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| Vue.js | 3.x | UI Framework (Composition API) |
| TypeScript | 5.x | Type-safe JavaScript |
| Vite | 5.x | Build tool & dev server |
| Pinia | 2.x | State management |
| TanStack Vue Query | 5.x | Server state & caching |
| Tailwind CSS | 3.x | Utility-first CSS |
| Shadcn Vue | latest | UI component library |
| VeeValidate | 4.x | Form validation |
| Zod | 3.x | Schema validation |
| ECharts | 5.x | Data visualization |
| Vue Router | 4.x | Client-side routing |
| Axios | 1.x | HTTP client |

### Backend
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| PHP | 8.2+ | Runtime |
| Laravel | 11 | Web framework |
| Laravel Sanctum | 4.x | SPA authentication |
| PostgreSQL Client | - | Database driver (pdo_pgsql) |
| Laravel HTTP Client | - | Service-to-service communication |
| Spatie Activity Log | 4.x | Audit logging |

### ML Engine
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| Python | 3.10+ | Runtime |
| FastAPI | 0.110+ | API framework |
| Uvicorn | 0.29+ | ASGI server |
| Pydantic | 2.x | Data validation |
| XGBoost | 2.x | ML model |
| NumPy | 1.x | Numerical computing |
| scikit-learn | 1.x | Preprocessing utilities |

### Infrastructure
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| Docker | 24+ | Containerization |
| Docker Compose | 2.x | Container orchestration |
| Nginx | 1.25+ | Reverse proxy & SSL |
| PostgreSQL | 15 | Relational database |

---

## 📋 Prasyarat

Sebelum memulai, pastikan sudah terinstal:

| Software | Versi Minimum | Cara Cek |
|----------|--------------|----------|
| Docker | 24.0+ | `docker --version` |
| Docker Compose | 2.20+ | `docker compose version` |
| Git | 2.40+ | `git --version` |
| Make (opsional) | 4.0+ | `make --version` |

### Persyaratan Hardware (Development)
- **CPU**: 4 cores
- **RAM**: 8 GB minimum (16 GB rekomendasi)
- **Disk**: 10 GB free space
- **OS**: Windows 10/11 (WSL2), macOS, Linux

### Persyaratan Hardware (Production)
- **CPU**: 8 cores
- **RAM**: 16 GB minimum
- **Disk**: 50 GB SSD
- **Network**: Static IP dengan domain

---

## 🚀 Instalasi & Deployment

### Quick Start (Development)

```bash
# 1. Clone repository
git clone https://github.com/your-org/hypertension-detection-system.git
cd hypertension-detection-system

# 2. Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env

# 3. Generate SSL certificates (development)
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/self-signed.key \
  -out nginx/ssl/self-signed.crt \
  -subj "/CN=localhost"

# 4. Build & Start semua services
docker compose up --build -d

# 5. Jalankan migrasi & seeder database
docker compose exec backend php artisan migrate --seed

# 6. Generate application key
docker compose exec backend php artisan key:generate

# 7. Akses aplikasi
# Frontend: https://localhost
# API Docs: https://localhost/api/documentation
```

### Makefile Commands

```bash
make up          # Start semua services
make down        # Stop semua services
make build       # Build ulang images
make migrate     # Jalankan migrasi
make seed        # Jalankan seeders
make fresh       # Fresh migration + seed
make logs        # Lihat logs semua services
make logs-ml     # Lihat logs ML Engine
make test-be     # Jalankan tests backend
make test-fe     # Jalankan tests frontend
make test-ml     # Jalankan tests ML Engine
make shell-be    # Shell ke backend container
make shell-ml    # Shell ke ML Engine container
make health      # Cek health semua services
```

### Production Deployment

```bash
# 1. Siapkan SSL certificate (Let's Encrypt)
# Edit nginx/conf.d/default.conf dengan path cert yang benar

# 2. Buat .env production
cp .env.example .env
# Edit .env dengan nilai production

# 3. Build & Deploy
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# 4. Migrasi production
docker compose exec backend php artisan migrate --force

# 5. Optimasi Laravel
docker compose exec backend php artisan config:cache
docker compose exec backend php artisan route:cache
docker compose exec backend php artisan view:cache
```

---

## ⚙️ Konfigurasi Environment

### Root `.env`

```env
# ========================
# APPLICATION
# ========================
APP_NAME="Sistem Deteksi Dini Risiko Hipertensi"
APP_ENV=local                    # local, staging, production
APP_DEBUG=true

# ========================
# DATABASE (PostgreSQL)
# ========================
DB_CONNECTION=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=hypertension_db
DB_USERNAME=hyper_admin
DB_PASSWORD=SecureP@ssw0rd!2024

# ========================
# ML ENGINE
# ========================
ML_ENGINE_HOST=ml-engine
ML_ENGINE_PORT=8000
ML_ENGINE_TIMEOUT=30
ML_ENGINE_RETRY_TIMES=3
ML_ENGINE_RETRY_SLEEP=500

# ========================
# NGINX
# ========================
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
```

### Backend `.env` (Laravel)

```env
APP_NAME="Hypertension API"
APP_ENV=local
APP_KEY=                         # Generated via artisan
APP_DEBUG=true
APP_URL=https://localhost

DB_CONNECTION=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=hypertension_db
DB_USERNAME=hyper_admin
DB_PASSWORD=SecureP@ssw0rd!2024

SANCTUM_STATEFUL_DOMAINS=localhost,localhost:443
SESSION_DOMAIN=localhost
SESSION_DRIVER=database

ML_ENGINE_BASE_URL=http://ml-engine:8000
ML_ENGINE_TIMEOUT=30
ML_ENGINE_RETRY_TIMES=3
```

---

## 🔄 Alur Kerja Sistem

### Alur 1: Login & Autentikasi

```
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  Browser │      │   Nginx  │      │  Laravel │      │ PostgreSQL│
│ (Vue.js) │      │  Proxy   │      │  Backend │      │  Database │
└────┬─────┘      └────┬─────┘      └────┬─────┘      └────┬─────┘
     │                  │                  │                  │
     │ GET /sanctum/    │                  │                  │
     │  csrf-cookie     │                  │                  │
     │─────────────────→│─────────────────→│                  │
     │                  │                  │                  │
     │   Set XSRF-TOKEN │                  │                  │
     │   (cookie)       │                  │                  │
     │←─────────────────│←─────────────────│                  │
     │                  │                  │                  │
     │ POST /api/login  │                  │                  │
     │ {email, password}│                  │                  │
     │ X-XSRF-TOKEN: .. │                 │                  │
     │─────────────────→│─────────────────→│                  │
     │                  │                  │                  │
     │                  │                  │  SELECT * FROM   │
     │                  │                  │  users WHERE     │
     │                  │                  │  email = ?       │
     │                  │                  │─────────────────→│
     │                  │                  │                  │
     │                  │                  │  User record     │
     │                  │                  │←─────────────────│
     │                  │                  │                  │
     │                  │                  │  Verify password │
     │                  │                  │  Create session  │
     │                  │                  │                  │
     │  Set-Cookie:     │                  │                  │
     │  session (HTTP-  │                  │                  │
     │  Only, Secure)   │                  │                  │
     │←─────────────────│←─────────────────│                  │
     │                  │                  │                  │
     │  ✅ Redirect to  │                  │                  │
     │  Dashboard       │                  │                  │
     │                  │                  │                  │
```

### Alur 2: Skrining Pasien (Main Flow)

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Browser │    │   Nginx  │    │  Laravel │    │  FastAPI │    │ XGBoost  │
│ (Vue.js) │    │  Proxy   │    │  Backend │    │ ML Engine│    │  Model   │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │               │
     │  ═══════════════════════════════════════════════════════════   │
     │  ║           STEP 1: Form Skrining (Client-Side)          ║   │
     │  ═══════════════════════════════════════════════════════════   │
     │               │               │               │               │
     │  User mengisi │               │               │               │
     │  form 4-step: │               │               │               │
     │  1. Identitas │               │               │               │
     │  2. Riwayat   │               │               │               │
     │  3. Gaya Hidup│               │               │               │
     │  4. Konfirmasi│               │               │               │
     │               │               │               │               │
     │  Zod + VeeValidate            │               │               │
     │  validasi real-time            │               │               │
     │               │               │               │               │
     │  ═══════════════════════════════════════════════════════════   │
     │  ║           STEP 2: Submit ke Backend                    ║   │
     │  ═══════════════════════════════════════════════════════════   │
     │               │               │               │               │
     │  POST /api/   │               │               │               │
     │   screenings  │               │               │               │
     │  {11 atribut} │               │               │               │
     │──────────────→│──────────────→│               │               │
     │               │               │               │               │
     │               │               │  FormRequest  │               │
     │               │               │  validation   │               │
     │               │               │  (server-side)│               │
     │               │               │               │               │
     │               │               │  Store patient│               │
     │               │               │  + screening  │               │
     │               │               │  to PostgreSQL│               │
     │               │               │               │               │
     │  ═══════════════════════════════════════════════════════════   │
     │  ║           STEP 3: Orkestrasi ke ML Engine              ║   │
     │  ═══════════════════════════════════════════════════════════   │
     │               │               │               │               │
     │               │               │  POST http:// │               │
     │               │               │  ml-engine:   │               │
     │               │               │  8000/predict │               │
     │               │               │  {11 features}│               │
     │               │               │──────────────→│               │
     │               │               │               │               │
     │               │               │               │  Pydantic v2  │
     │               │               │               │  validate I/O │
     │               │               │               │               │
     │  ═══════════════════════════════════════════════════════════   │
     │  ║           STEP 4: ML Pipeline                          ║   │
     │  ═══════════════════════════════════════════════════════════   │
     │               │               │               │               │
     │               │               │               │  Label Encode │
     │               │               │               │  (static map) │
     │               │               │               │               │
     │               │               │               │  MinMax Scale │
     │               │               │               │  (hardcoded   │
     │               │               │               │   min/max)    │
     │               │               │               │               │
     │               │               │               │  ────────────→│
     │               │               │               │               │
     │               │               │               │  XGBoost      │
     │               │               │               │  .predict()   │
     │               │               │               │  .predict_    │
     │               │               │               │   proba()     │
     │               │               │               │               │
     │               │               │               │  ←────────────│
     │               │               │               │               │
     │               │               │               │  Feature      │
     │               │               │               │  Importance   │
     │               │               │               │  (SHAP/gain)  │
     │               │               │               │               │
     │  ═══════════════════════════════════════════════════════════   │
     │  ║           STEP 5: Response & Visualisasi               ║   │
     │  ═══════════════════════════════════════════════════════════   │
     │               │               │               │               │
     │               │               │  {prediction, │               │
     │               │               │   confidence, │               │
     │               │               │   features}   │               │
     │               │               │←──────────────│               │
     │               │               │               │               │
     │               │               │  Store        │               │
     │               │               │  prediction   │               │
     │               │               │  to PostgreSQL│               │
     │               │               │               │               │
     │               │               │  Log activity │               │
     │               │               │  (sanitized)  │               │
     │               │               │               │               │
     │  JSON Response│               │               │               │
     │  {risk_level, │               │               │               │
     │   confidence, │               │               │               │
     │   feature_    │               │               │               │
     │   importance} │               │               │               │
     │←──────────────│←──────────────│               │               │
     │               │               │               │               │
     │  Render:      │               │               │               │
     │  - Risk Badge │               │               │               │
     │  - Confidence │               │               │               │
     │    Gauge      │               │               │               │
     │  - Feature    │               │               │               │
     │    Importance │               │               │               │
     │    Chart      │               │               │               │
     │  - ECharts    │               │               │               │
     │    Dashboard  │               │               │               │
     │               │               │               │               │
```

### Alur 3: RBAC Access Control

```
┌──────────────────────────────────────────────────────┐
│                    ROLE HIERARCHY                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │              SUPER ADMIN                        │ │
│  │  ✅ Manajemen User (CRUD)                       │ │
│  │  ✅ Lihat Audit Log                             │ │
│  │  ✅ Dashboard Analytics                         │ │
│  │  ✅ Semua fitur Dokter                          │ │
│  │  ✅ Semua fitur Perawat                         │ │
│  └─────────────────────────────────────────────────┘ │
│                       │                              │
│                       ▼                              │
│  ┌─────────────────────────────────────────────────┐ │
│  │                DOKTER                            │ │
│  │  ✅ Skrining Pasien                             │ │
│  │  ✅ Lihat Hasil Prediksi                        │ │
│  │  ✅ Dashboard XAI (Feature Importance)          │ │
│  │  ✅ Lihat Riwayat Semua Pasien                  │ │
│  │  ✅ Export Laporan                              │ │
│  │  ❌ Manajemen User                              │ │
│  │  ❌ Audit Log                                   │ │
│  └─────────────────────────────────────────────────┘ │
│                       │                              │
│                       ▼                              │
│  ┌─────────────────────────────────────────────────┐ │
│  │               PERAWAT                            │ │
│  │  ✅ Skrining Pasien                             │ │
│  │  ✅ Lihat Hasil Prediksi (sendiri)              │ │
│  │  ✅ Lihat Riwayat Pasien (sendiri)              │ │
│  │  ❌ Dashboard XAI                               │ │
│  │  ❌ Export Laporan                              │ │
│  │  ❌ Manajemen User                              │ │
│  │  ❌ Audit Log                                   │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 📡 API Documentation

### Authentication Endpoints

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| `GET` | `/sanctum/csrf-cookie` | Ambil CSRF token | ❌ |
| `POST` | `/api/login` | Login user | ❌ |
| `POST` | `/api/logout` | Logout user | ✅ |
| `GET` | `/api/user` | Profil user aktif | ✅ |

### Screening Endpoints

| Method | Endpoint | Deskripsi | Auth | Role |
|--------|----------|-----------|------|------|
| `GET` | `/api/screenings` | Daftar skrining | ✅ | All |
| `POST` | `/api/screenings` | Buat skrining baru | ✅ | Dokter, Perawat |
| `GET` | `/api/screenings/{id}` | Detail skrining | ✅ | All |
| `GET` | `/api/screenings/{id}/prediction` | Hasil prediksi | ✅ | Dokter |

### Patient Endpoints

| Method | Endpoint | Deskripsi | Auth | Role |
|--------|----------|-----------|------|------|
| `GET` | `/api/patients` | Daftar pasien | ✅ | All |
| `POST` | `/api/patients` | Tambah pasien | ✅ | All |
| `GET` | `/api/patients/{id}` | Detail pasien | ✅ | All |
| `GET` | `/api/patients/{id}/screenings` | Riwayat skrining | ✅ | All |

### Dashboard Endpoints

| Method | Endpoint | Deskripsi | Auth | Role |
|--------|----------|-----------|------|------|
| `GET` | `/api/dashboard/stats` | Statistik overview | ✅ | Dokter, Admin |
| `GET` | `/api/dashboard/risk-distribution` | Distribusi risiko | ✅ | Dokter, Admin |
| `GET` | `/api/dashboard/feature-importance` | Feature importance | ✅ | Dokter, Admin |

### Admin Endpoints

| Method | Endpoint | Deskripsi | Auth | Role |
|--------|----------|-----------|------|------|
| `GET` | `/api/admin/users` | Daftar user | ✅ | Admin |
| `POST` | `/api/admin/users` | Buat user baru | ✅ | Admin |
| `PUT` | `/api/admin/users/{id}` | Update user | ✅ | Admin |
| `DELETE` | `/api/admin/users/{id}` | Hapus user | ✅ | Admin |
| `GET` | `/api/admin/audit-logs` | Log aktivitas | ✅ | Admin |

### Health Check Endpoints

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| `GET` | `/api/health` | Laravel health | ❌ |
| `GET` | `ml-engine:8000/health` | ML Engine health | Internal |
| `GET` | `ml-engine:8000/health/model` | Model status | Internal |

### Contoh Request & Response

#### POST `/api/screenings`

**Request:**
```json
{
  "patient": {
    "name": "Ahmad Sudrajat",
    "nik": "3201234567890001",
    "date_of_birth": "1975-03-15",
    "gender": "male"
  },
  "screening_data": {
    "age": 48,
    "gender": "male",
    "bmi": 28.5,
    "smoking_status": "former",
    "alcohol_consumption": "moderate",
    "physical_activity": "low",
    "family_history": true,
    "diabetes": false,
    "systolic_bp": 135,
    "diastolic_bp": 88,
    "cholesterol_level": "high"
  }
}
```

**Response (201):**
```json
{
  "data": {
    "id": "scr_2024_00001",
    "patient_id": "pat_2024_00042",
    "screened_by": {
      "id": 3,
      "name": "Dr. Siti Aminah",
      "role": "dokter"
    },
    "screening_data": {
      "age": 48,
      "gender": "male",
      "bmi": 28.5,
      "...": "..."
    },
    "prediction": {
      "risk_level": "high",
      "risk_label": "Risiko Tinggi",
      "confidence_score": 0.87,
      "probability": {
        "low": 0.08,
        "medium": 0.05,
        "high": 0.87
      },
      "feature_importance": [
        { "feature": "systolic_bp", "importance": 0.234, "label": "Tekanan Darah Sistolik" },
        { "feature": "bmi", "importance": 0.189, "label": "Indeks Massa Tubuh" },
        { "feature": "age", "importance": 0.156, "label": "Usia" },
        { "feature": "family_history", "importance": 0.134, "label": "Riwayat Keluarga" },
        { "feature": "cholesterol_level", "importance": 0.098, "label": "Kadar Kolesterol" },
        { "feature": "physical_activity", "importance": 0.067, "label": "Aktivitas Fisik" },
        { "feature": "smoking_status", "importance": 0.045, "label": "Status Merokok" },
        { "feature": "diastolic_bp", "importance": 0.038, "label": "Tekanan Darah Diastolik" },
        { "feature": "diabetes", "importance": 0.022, "label": "Diabetes" },
        { "feature": "alcohol_consumption", "importance": 0.012, "label": "Konsumsi Alkohol" },
        { "feature": "gender", "importance": 0.005, "label": "Jenis Kelamin" }
      ]
    },
    "created_at": "2024-11-15T10:30:00Z"
  }
}
```

---

## 🤖 ML Engine Pipeline

### 11 Atribut Klinis (Features)

| # | Feature | Tipe | Range/Values | Deskripsi |
|---|---------|------|-------------|-----------|
| 1 | `age` | Numerik | 18-100 | Usia pasien (tahun) |
| 2 | `gender` | Kategorikal | male, female | Jenis kelamin |
| 3 | `bmi` | Numerik | 10.0-60.0 | Body Mass Index (kg/m²) |
| 4 | `smoking_status` | Kategorikal | never, former, current | Status merokok |
| 5 | `alcohol_consumption` | Kategorikal | none, moderate, heavy | Konsumsi alkohol |
| 6 | `physical_activity` | Kategorikal | low, moderate, high | Tingkat aktivitas fisik |
| 7 | `family_history` | Boolean | true, false | Riwayat hipertensi keluarga |
| 8 | `diabetes` | Boolean | true, false | Riwayat diabetes |
| 9 | `systolic_bp` | Numerik | 70-250 | Tekanan darah sistolik (mmHg) |
| 10 | `diastolic_bp` | Numerik | 40-150 | Tekanan darah diastolik (mmHg) |
| 11 | `cholesterol_level` | Kategorikal | normal, borderline, high | Kadar kolesterol |

### Pipeline Prapemrosesan Deterministik

```python
# STATIC LABEL ENCODING MAP (dari distribusi data latih)
LABEL_ENCODING = {
    "gender":              {"male": 0, "female": 1},
    "smoking_status":      {"never": 0, "former": 1, "current": 2},
    "alcohol_consumption": {"none": 0, "moderate": 1, "heavy": 2},
    "physical_activity":   {"low": 0, "moderate": 1, "high": 2},
    "family_history":      {False: 0, True: 1},
    "diabetes":            {False: 0, True: 1},
    "cholesterol_level":   {"normal": 0, "borderline": 1, "high": 2},
}

# STATIC MIN-MAX SCALING (hardcoded dari data latih)
# Mencegah data leakage — nilai dikunci berdasarkan distribusi training set
FEATURE_RANGES = {
    "age":            {"min": 18,   "max": 100},
    "gender":         {"min": 0,    "max": 1},
    "bmi":            {"min": 10.0, "max": 55.0},
    "smoking_status": {"min": 0,    "max": 2},
    "alcohol_consumption": {"min": 0, "max": 2},
    "physical_activity":   {"min": 0, "max": 2},
    "family_history": {"min": 0,    "max": 1},
    "diabetes":       {"min": 0,    "max": 1},
    "systolic_bp":    {"min": 70,   "max": 250},
    "diastolic_bp":   {"min": 40,   "max": 150},
    "cholesterol_level": {"min": 0, "max": 2},
}

# Formula MinMax: X_scaled = (X - X_min) / (X_max - X_min)
```

### XGBoost Model Parameters (SGO-Optimized)

```python
MODEL_PARAMS = {
    "objective":      "binary:logistic",   # Binary classification
    "eval_metric":    "logloss",
    "learning_rate":  0.035,               # SGO-optimized
    "max_depth":      9,                   # SGO-optimized
    "n_estimators":   285,                 # SGO-optimized
    "subsample":      0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 3,
    "gamma":          0.1,
    "reg_alpha":      0.1,
    "reg_lambda":     1.0,
    "random_state":   42,
    "use_label_encoder": False,
}
```

### Pipeline Flow

```
Input (11 features)
       │
       ▼
┌─────────────────┐
│ Pydantic v2     │ ← Validasi tipe, range, required fields
│ Input Schema    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Label Encoding  │ ← Static map (gender, smoking, alcohol, etc.)
│ (Categorical →  │
│  Numeric)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MinMax Scaling  │ ← Static min/max (hardcoded dari training set)
│ [0, 1] range    │    Formula: (X - X_min) / (X_max - X_min)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ XGBoost Model   │ ← Loaded from static .json artifact
│ .predict()      │    SGO params: lr=0.035, depth=9, n=285
│ .predict_proba()│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Feature         │ ← Dari model.feature_importances_ (gain-based)
│ Importance      │
│ Extraction      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pydantic v2     │ ← Validasi output sebelum dikirim
│ Output Schema   │
└────────┬────────┘
         │
         ▼
Response JSON
{risk_level, confidence, feature_importance[]}
```

---

## 🎨 Frontend Components

### Multi-Step Screening Form

```
┌────────────────────────────────────────────────────────────────┐
│                    FORM SKRINING PASIEN                        │
│                                                                │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐           │
│  │ Step 1 │──→│ Step 2 │──→│ Step 3 │──→│ Step 4 │           │
│  │Identitas│   │Riwayat │   │Gaya    │   │Konfir- │           │
│  │ Pasien │   │ Medis  │   │Hidup   │   │masi    │           │
│  └────────┘   └────────┘   └────────┘   └────────┘           │
│  ●───────────○───────────○───────────○  Progress Bar          │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                          │  │
│  │  Step 1: Identitas Pasien                                │  │
│  │  ─────────────────────────                               │  │
│  │                                                          │  │
│  │  ┌──────────────────┐  ┌──────────────────┐              │  │
│  │  │ Nama Lengkap     │  │ NIK              │              │  │
│  │  │ ________________ │  │ ________________ │              │  │
│  │  └──────────────────┘  └──────────────────┘              │  │
│  │                                                          │  │
│  │  ┌──────────────────┐  ┌──────────────────┐              │  │
│  │  │ Tanggal Lahir    │  │ Jenis Kelamin    │              │  │
│  │  │ ____/____/______ │  │ ▼ Pilih...       │              │  │
│  │  └──────────────────┘  └──────────────────┘              │  │
│  │                                                          │  │
│  │  ┌──────────────────┐                                    │  │
│  │  │ Usia (auto-calc) │                                    │  │
│  │  │ ____ tahun       │                                    │  │
│  │  └──────────────────┘                                    │  │
│  │                                                          │  │
│  │                        ┌──────────────┐                  │  │
│  │                        │  Selanjutnya →│                  │  │
│  │                        └──────────────┘                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### XAI Dashboard Wireframe

```
┌────────────────────────────────────────────────────────────────────────────┐
│  📊 Dashboard Explainable AI                                    🌓 Toggle │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐           │
│  │ 📈 Total Skrining │ │ 🔴 Risiko Tinggi │ │ 🟢 Risiko Rendah │           │
│  │     1,247         │ │     342 (27.4%)  │ │     698 (55.9%)  │           │
│  │   ↑ 12% bulan ini │ │   ↓ 3% bulan ini │ │   ↑ 8% bulan ini │           │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘           │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                  FEATURE IMPORTANCE CHART (ECharts)                  │  │
│  │                                                                      │  │
│  │  Tekanan Darah Sistolik  ████████████████████████████████  23.4%     │  │
│  │  Indeks Massa Tubuh      █████████████████████████         18.9%     │  │
│  │  Usia                    ████████████████████              15.6%     │  │
│  │  Riwayat Keluarga        ██████████████████                13.4%     │  │
│  │  Kadar Kolesterol        ████████████                       9.8%     │  │
│  │  Aktivitas Fisik         ████████                           6.7%     │  │
│  │  Status Merokok          ██████                             4.5%     │  │
│  │  Tekanan Darah Diastolik █████                              3.8%     │  │
│  │  Diabetes                ███                                2.2%     │  │
│  │  Konsumsi Alkohol        ██                                 1.2%     │  │
│  │  Jenis Kelamin           █                                  0.5%     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐       │
│  │  DISTRIBUSI RISIKO (Donut)   │  │  TREND BULANAN (Line Chart) │       │
│  │                              │  │                              │       │
│  │       ┌──────┐               │  │      ╱╲    ╱╲               │       │
│  │      /  27%  \              │  │     ╱  ╲  ╱  ╲              │       │
│  │     | HIGH   |              │  │    ╱    ╲╱    ╲             │       │
│  │     | 56%LOW |              │  │   ╱              ╲          │       │
│  │      \  17%  /              │  │  ╱                ╲         │       │
│  │       └──────┘               │  │ ╱                  ╲       │       │
│  │   ● High  ● Medium  ● Low   │  │ Jan Feb Mar Apr May Jun     │       │
│  └──────────────────────────────┘  └──────────────────────────────┘       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌──────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│      users       │     │      patients         │     │     screenings       │
├──────────────────┤     ├──────────────────────┤     ├──────────────────────┤
│ id         (PK)  │     │ id             (PK)  │     │ id             (PK)  │
│ name             │     │ name                 │     │ patient_id     (FK)──┤──→ patients.id
│ email     (UQ)   │     │ nik          (UQ)    │     │ user_id        (FK)──┤──→ users.id
│ password         │     │ date_of_birth        │     │ age                  │
│ role             │     │ gender               │     │ gender               │
│ is_active        │     │ address              │     │ bmi                  │
│ email_verified_at│     │ phone                │     │ smoking_status       │
│ created_at       │     │ created_at           │     │ alcohol_consumption  │
│ updated_at       │     │ updated_at           │     │ physical_activity    │
└──────────────────┘     │ deleted_at           │     │ family_history       │
         │               └──────────────────────┘     │ diabetes             │
         │                        │                    │ systolic_bp          │
         │                        │                    │ diastolic_bp         │
         │                        │                    │ cholesterol_level    │
         │                        │                    │ created_at           │
         │                        │                    │ updated_at           │
         │                        │                    └──────────────────────┘
         │                        │                              │
         │                        │                              │
         ▼                        │                              ▼
┌──────────────────┐              │              ┌──────────────────────┐
│  activity_logs   │              │              │     predictions      │
├──────────────────┤              │              ├──────────────────────┤
│ id         (PK)  │              │              │ id             (PK)  │
│ user_id    (FK)──┤──────────────┘              │ screening_id   (FK)──┤──→ screenings.id
│ action           │                             │ risk_level           │
│ entity_type      │                             │ confidence_score     │
│ entity_id        │                             │ probability_low      │
│ description      │                             │ probability_medium   │
│ ip_address       │                             │ probability_high     │
│ user_agent       │                             │ feature_importance   │  ← JSON column
│ created_at       │                             │ model_version        │
└──────────────────┘                             │ inference_time_ms    │
                                                 │ created_at           │
                                                 └──────────────────────┘
```

### Migrasi Laravel

```php
// Migration: create_users_table
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email')->unique();
    $table->string('password');
    $table->enum('role', ['super_admin', 'dokter', 'perawat'])->default('perawat');
    $table->boolean('is_active')->default(true);
    $table->timestamp('email_verified_at')->nullable();
    $table->rememberToken();
    $table->timestamps();
});

// Migration: create_patients_table
Schema::create('patients', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('nik', 16)->unique();
    $table->date('date_of_birth');
    $table->enum('gender', ['male', 'female']);
    $table->text('address')->nullable();
    $table->string('phone', 15)->nullable();
    $table->timestamps();
    $table->softDeletes();
});

// Migration: create_screenings_table
Schema::create('screenings', function (Blueprint $table) {
    $table->id();
    $table->foreignId('patient_id')->constrained()->cascadeOnDelete();
    $table->foreignId('user_id')->constrained();
    $table->integer('age');
    $table->enum('gender', ['male', 'female']);
    $table->decimal('bmi', 5, 2);
    $table->enum('smoking_status', ['never', 'former', 'current']);
    $table->enum('alcohol_consumption', ['none', 'moderate', 'heavy']);
    $table->enum('physical_activity', ['low', 'moderate', 'high']);
    $table->boolean('family_history');
    $table->boolean('diabetes');
    $table->integer('systolic_bp');
    $table->integer('diastolic_bp');
    $table->enum('cholesterol_level', ['normal', 'borderline', 'high']);
    $table->timestamps();
});

// Migration: create_predictions_table
Schema::create('predictions', function (Blueprint $table) {
    $table->id();
    $table->foreignId('screening_id')->constrained()->cascadeOnDelete();
    $table->enum('risk_level', ['low', 'medium', 'high']);
    $table->decimal('confidence_score', 5, 4);
    $table->decimal('probability_low', 5, 4);
    $table->decimal('probability_medium', 5, 4);
    $table->decimal('probability_high', 5, 4);
    $table->json('feature_importance');
    $table->string('model_version');
    $table->integer('inference_time_ms');
    $table->timestamps();
});

// Migration: create_activity_logs_table
Schema::create('activity_logs', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained();
    $table->string('action');         // e.g., 'screening.created'
    $table->string('entity_type');    // e.g., 'App\Models\Screening'
    $table->unsignedBigInteger('entity_id')->nullable();
    $table->string('description');    // Sanitized description
    $table->ipAddress('ip_address')->nullable();
    $table->string('user_agent')->nullable();
    $table->timestamps();

    $table->index(['entity_type', 'entity_id']);
    $table->index('user_id');
});
```

---

## 🔒 Keamanan

### Security Checklist

| Layer | Implementasi | Status |
|-------|-------------|--------|
| **Transport** | SSL/TLS via Nginx (HTTPS enforced) | ✅ |
| **Authentication** | Laravel Sanctum (HTTP-Only Cookie) | ✅ |
| **Authorization** | RBAC Middleware (3 role levels) | ✅ |
| **Input Validation** | Laravel Form Requests + Pydantic v2 | ✅ |
| **XSS Prevention** | HTTP-Only cookies, CSP headers | ✅ |
| **CSRF Protection** | Sanctum CSRF token | ✅ |
| **SQL Injection** | Eloquent ORM parameterized queries | ✅ |
| **Network Isolation** | Docker internal network | ✅ |
| **Data Masking** | Sanitized audit logs (no PHI) | ✅ |
| **Security Headers** | X-Frame-Options, X-Content-Type-Options, etc. | ✅ |
| **Rate Limiting** | Laravel rate limiter on API endpoints | ✅ |
| **Password Hashing** | Bcrypt with cost factor 12 | ✅ |

### Nginx Security Headers

```nginx
# Security Headers (snippets/security-headers.conf)
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:;" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
```

---

## 📊 Monitoring & Logging

### Health Check Matrix

| Service | Endpoint | Interval | Expected |
|---------|----------|----------|----------|
| Nginx | TCP :443 | 10s | Connection OK |
| Frontend | HTTP /index.html | 30s | 200 OK |
| Backend | GET /api/health | 15s | 200 + DB OK |
| ML Engine | GET /health | 15s | 200 + Model loaded |
| PostgreSQL | pg_isready | 10s | Exit 0 |

### Log Locations (Inside Containers)

```
nginx:      /var/log/nginx/access.log, /var/log/nginx/error.log
backend:    /var/www/html/storage/logs/laravel.log
ml-engine:  stdout/stderr (captured by Docker)
postgres:   /var/log/postgresql/postgresql-15-main.log
```

### Docker Log Commands

```bash
# Lihat semua logs
docker compose logs -f

# Lihat logs spesifik service
docker compose logs -f backend
docker compose logs -f ml-engine
docker compose logs -f nginx

# Filter by timestamp
docker compose logs --since="2024-01-01T00:00:00" backend
```

---

## ❗ Troubleshooting

### Masalah Umum

<details>
<summary><strong>🔴 Error: "Connection refused" ke ML Engine</strong></summary>

**Penyebab:** ML Engine belum selesai loading model saat Backend mencoba connect.

**Solusi:**
```bash
# Cek status ML Engine
docker compose logs ml-engine

# Pastikan health check OK
docker compose exec backend curl http://ml-engine:8000/health

# Restart ML Engine
docker compose restart ml-engine
```
</details>

<details>
<summary><strong>🔴 Error: "CSRF token mismatch"</strong></summary>

**Penyebab:** Domain Sanctum tidak match atau cookie expired.

**Solusi:**
1. Pastikan `SANCTUM_STATEFUL_DOMAINS` di `.env` sesuai
2. Pastikan `SESSION_DOMAIN` benar
3. Clear browser cookies dan re-login
</details>

<details>
<summary><strong>🔴 Error: PostgreSQL "Connection refused"</strong></summary>

**Penyebab:** PostgreSQL belum ready saat Laravel mencoba connect.

**Solusi:**
```bash
# Cek apakah PostgreSQL ready
docker compose exec postgres pg_isready

# Pastikan depends_on dengan health check
# Sudah dikonfigurasi di docker-compose.yml
```
</details>

<details>
<summary><strong>🔴 Frontend blank screen (white page)</strong></summary>

**Penyebab:** Build Vue gagal atau nginx proxy misconfigured.

**Solusi:**
```bash
# Cek nginx logs
docker compose logs nginx

# Cek frontend build
docker compose logs frontend

# Rebuild frontend
docker compose build frontend --no-cache
```
</details>

<details>
<summary><strong>🟡 Prediksi model lambat (> 1 detik)</strong></summary>

**Penyebab:** Model loading ulang di setiap request (cold start).

**Solusi:**
Model di-load saat startup (`@app.on_event("startup")`), bukan per-request. Cek apakah model sudah di-cache:
```bash
docker compose exec ml-engine curl http://localhost:8000/health/model
```
</details>

---

## 🤝 Kontribusi

### Branch Naming Convention

```
feature/HYP-001-login-page
bugfix/HYP-015-csrf-token-mismatch
hotfix/HYP-022-model-loading-error
chore/HYP-030-update-dependencies
```

### Commit Convention

```
feat: add multi-step screening form with Zod validation
fix: resolve CSRF token mismatch on Sanctum login
docs: update API documentation for screening endpoint
refactor: extract ML preprocessing into separate module
test: add unit tests for MinMax scaling pipeline
chore: bump XGBoost to v2.0.3
```

### Pull Request Checklist

- [ ] Kode telah di-test secara lokal
- [ ] Unit tests ditambahkan/diperbarui
- [ ] Migrasi database sudah di-test
- [ ] Dokumentasi API diperbarui
- [ ] Tidak ada data medis sensitif yang ter-log
- [ ] Docker build berhasil
- [ ] Semua health checks hijau

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat file [LICENSE](LICENSE) untuk detail.

---

## 👥 Tim Pengembang

| Peran | Tanggung Jawab |
|-------|---------------|
| **Lead DevOps Engineer** | Docker, Nginx, CI/CD, Network Architecture |
| **MLOps Architect** | XGBoost Pipeline, FastAPI, Model Serving |
| **Senior Full-Stack Developer** | Laravel API, Vue.js SPA, Database Design |
| **UI/UX Expert** | Shadcn Vue, Tailwind CSS, Dark Mode, Animations |

---

<p align="center">
  <strong>Sistem Deteksi Dini Risiko Hipertensi</strong><br>
  Built with ❤️ for better healthcare
</p>
