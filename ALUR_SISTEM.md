# 🔄 ALUR SISTEM — Sistem Deteksi Dini Risiko Hipertensi

> Dokumen ini menjelaskan secara detail setiap alur (flow) dalam sistem, dari interaksi pengguna hingga proses internal antar microservices.

---

## Daftar Alur

1. [Alur Startup Sistem](#1-alur-startup-sistem)
2. [Alur Autentikasi (Login/Logout)](#2-alur-autentikasi-loginlogout)
3. [Alur Skrining Pasien (Core Flow)](#3-alur-skrining-pasien-core-flow)
4. [Alur ML Prediction Pipeline](#4-alur-ml-prediction-pipeline)
5. [Alur Dashboard XAI](#5-alur-dashboard-xai)
6. [Alur RBAC & Authorization](#6-alur-rbac--authorization)
7. [Alur Manajemen User (Admin)](#7-alur-manajemen-user-admin)
8. [Alur Error Handling & Recovery](#8-alur-error-handling--recovery)
9. [Alur Data Persistence](#9-alur-data-persistence)
10. [Alur Dark/Light Mode](#10-alur-darklight-mode)

---

## 🚧 Status Pengembangan (Progress Checklist)
- [x] **Fase Perencanaan**: Pembuatan README, WALKTHROUGH, dan ALUR SISTEM.
- [x] **Implementasi**: Alur 1 - Startup Sistem.
- [x] **Implementasi**: Alur 2 - Autentikasi.
- [x] **Implementasi**: Alur 3 - Skrining Pasien.
- [x] **Implementasi**: Alur 4 - ML Prediction Pipeline.
- [x] **Implementasi**: Alur 5 - Dashboard XAI.
- [x] **Implementasi**: Alur 6 - RBAC & Authorization.
- [x] **Implementasi**: Alur 7 - Manajemen User.
- [x] **Implementasi**: Alur 8 - Error Handling.
- [x] **Implementasi**: Alur 9 - Data Persistence.
- [x] **Implementasi**: Alur 10 - Dark/Light Mode.

---

## 1. Alur Startup Sistem

### Urutan Boot Services

```
docker compose up -d
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│ BOOT SEQUENCE (Berdasarkan depends_on + healthcheck)           │
│                                                                 │
│  T+0s   ┌──────────────┐                                      │
│  ────→  │ PostgreSQL 15 │  ← Boot pertama (tidak ada dependency)│
│         │ Port: 5432    │                                      │
│         └──────┬───────┘                                      │
│                │ healthcheck: pg_isready (setiap 10s)          │
│                │                                                │
│  T+10s  ┌─────▼────────┐                                      │
│  ────→  │ ML Engine    │  ← Setelah PostgreSQL healthy         │
│         │ FastAPI :8000 │     (opsional, bisa paralel)          │
│         └──────┬───────┘                                      │
│                │ lifespan: Load XGBoost model ke memory         │
│                │ healthcheck: GET /health (setiap 15s)          │
│                │                                                │
│  T+30s  ┌─────▼────────┐                                      │
│  ────→  │ Backend      │  ← Setelah PostgreSQL + ML Engine OK  │
│         │ Laravel :9000 │                                      │
│         └──────┬───────┘                                      │
│                │ healthcheck: php artisan health:check          │
│                │                                                │
│  T+45s  ┌─────▼────────┐                                      │
│  ────→  │ Frontend     │  ← Setelah Backend OK                 │
│         │ Vue.js :5173  │                                      │
│         └──────┬───────┘                                      │
│                │                                                │
│  T+50s  ┌─────▼────────┐                                      │
│  ────→  │ Nginx        │  ← Setelah Backend + Frontend OK     │
│         │ :80, :443     │                                      │
│         └──────────────┘                                      │
│                                                                 │
│  T+60s  ✅ SISTEM SIAP DIAKSES                                │
│         https://localhost                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Health Check Cascade

```
Nginx (setiap 30s)
├── nginx -t → Konfigurasi valid?
└── ✅ Healthy

Backend (setiap 30s)
├── Database connection → OK?
├── Session store → OK?
├── ML Engine reachable → OK?
└── ✅ Healthy

ML Engine (setiap 15s)
├── Model loaded in memory → OK?
├── Preprocessing pipeline initialized → OK?
└── ✅ Healthy

PostgreSQL (setiap 10s)
├── pg_isready → Accepting connections?
└── ✅ Healthy
```

---

## 2. Alur Autentikasi (Login/Logout)

### 2.1 Login Flow (Laravel Sanctum SPA)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          LOGIN FLOW                                      │
│                                                                           │
│  BROWSER (Vue.js)                                                         │
│  │                                                                        │
│  │ ① User membuka halaman login                                          │
│  │   Vue Router → /login → LoginPage.vue                                 │
│  │                                                                        │
│  │ ② User mengisi email & password                                       │
│  │   VeeValidate + Zod: validasi format email, min length password       │
│  │                                                                        │
│  │ ③ Sebelum submit, ambil CSRF token                                    │
│  │   GET https://localhost/sanctum/csrf-cookie                           │
│  │   │                                                                    │
│  │   │ → Nginx proxy → Backend Laravel                                   │
│  │   │                                                                    │
│  │   │ ← Set-Cookie: XSRF-TOKEN=abc123... (regular cookie, readable JS) │
│  │   │ ← Set-Cookie: laravel_session=... (HTTP-Only, NOT readable JS)    │
│  │                                                                        │
│  │ ④ Submit login request                                                │
│  │   POST https://localhost/api/login                                    │
│  │   Headers:                                                            │
│  │     Content-Type: application/json                                    │
│  │     X-XSRF-TOKEN: abc123...  (dari cookie XSRF-TOKEN)               │
│  │     Accept: application/json                                          │
│  │   Body:                                                               │
│  │     { "email": "dokter@hypertension.id", "password": "password" }    │
│  │   │                                                                    │
│  │   │ → Nginx proxy → Backend Laravel                                   │
│  │   │                                                                    │
│  │   │   Backend:                                                        │
│  │   │   ├── Verify CSRF token ✅                                        │
│  │   │   ├── Find user by email → PostgreSQL                            │
│  │   │   ├── Verify password (bcrypt) ✅                                 │
│  │   │   ├── Regenerate session ID (prevent fixation)                   │
│  │   │   ├── Log activity: "user.login" (IP, timestamp, NO password)    │
│  │   │   └── Return user data + role                                    │
│  │   │                                                                    │
│  │   │ ← 200 OK                                                         │
│  │   │ ← Set-Cookie: laravel_session=NEW_SESSION (HTTP-Only, Secure)    │
│  │   │ ← Body: { "user": { "id":3, "name":"Dr. Siti", "role":"dokter" }}│
│  │                                                                        │
│  │ ⑤ Frontend updates state                                             │
│  │   authStore.user = response.user                                      │
│  │   authStore.isAuthenticated = true                                    │
│  │   │                                                                    │
│  │   │ → Vue Router: redirect ke /dashboard                             │
│  │   │ → Toast: "✅ Selamat datang, Dr. Siti!"                          │
│  │                                                                        │
└───────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Authenticated Request Flow

```
Setiap API Request setelah login:

Browser (Axios interceptor)
│
├── Otomatis kirim cookie (withCredentials: true)
│   Cookie: laravel_session=SESSION_ID
│   Cookie: XSRF-TOKEN=CSRF_TOKEN
│
├── Axios interceptor menambahkan header:
│   X-XSRF-TOKEN: CSRF_TOKEN (dari cookie)
│
▼
Nginx → Backend Laravel
│
├── 1. VerifyCsrfToken middleware → Cek X-XSRF-TOKEN ✅
├── 2. StartSession middleware → Load session dari cookie ✅
├── 3. auth:sanctum middleware → User authenticated? ✅
├── 4. RoleMiddleware → User punya akses ke route ini? ✅
│
├── ✅ Lanjut ke Controller
│
└── ❌ 401 Unauthenticated
    └── Frontend: Redirect ke /login, clear authStore
```

### 2.3 Logout Flow

```
User klik Logout
│
├── POST /api/logout
│   Cookie: laravel_session=SESSION_ID
│
├── Backend:
│   ├── Invalidate session
│   ├── Regenerate CSRF token
│   ├── Log activity: "user.logout"
│   └── Return 204 No Content
│
├── Frontend:
│   ├── authStore.user = null
│   ├── authStore.isAuthenticated = false
│   ├── queryClient.clear() (TanStack Query cache)
│   └── Router.push('/login')
│
└── ✅ User kembali ke halaman login
```

---

## 3. Alur Skrining Pasien (Core Flow)

### 3.1 Sequence Diagram Detail

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Vue.js  │    │  Nginx   │    │  Laravel │    │  FastAPI │    │PostgreSQL│
│ Frontend │    │  Proxy   │    │  Backend │    │ ML Engine│    │ Database │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │               │
     │ ═══ FASE 1: PENGISIAN FORM (Client-Side Only) ═══            │
     │               │               │               │               │
     │ User navigasi ke              │               │               │
     │ /screening/new                │               │               │
     │               │               │               │               │
     │ Step 1: Identitas Pasien      │               │               │
     │ ├── Nama, NIK, Tanggal Lahir  │               │               │
     │ ├── Jenis Kelamin             │               │               │
     │ ├── Usia (auto-calculated)    │               │               │
     │ └── Zod validation ✅         │               │               │
     │               │               │               │               │
     │ Step 2: Riwayat Medis         │               │               │
     │ ├── Tekanan Darah Sistolik    │               │               │
     │ ├── Tekanan Darah Diastolik   │               │               │
     │ ├── BMI                       │               │               │
     │ ├── Riwayat Keluarga          │               │               │
     │ ├── Diabetes                  │               │               │
     │ ├── Kadar Kolesterol          │               │               │
     │ └── Zod validation ✅         │               │               │
     │               │               │               │               │
     │ Step 3: Gaya Hidup            │               │               │
     │ ├── Status Merokok            │               │               │
     │ ├── Konsumsi Alkohol          │               │               │
     │ ├── Aktivitas Fisik           │               │               │
     │ └── Zod validation ✅         │               │               │
     │               │               │               │               │
     │ Step 4: Konfirmasi            │               │               │
     │ ├── Review semua data         │               │               │
     │ └── User klik "Proses"        │               │               │
     │               │               │               │               │
     │ ═══ FASE 2: SUBMIT KE BACKEND ═══                            │
     │               │               │               │               │
     │ TanStack Query│               │               │               │
     │ useMutation() │               │               │               │
     │ ─ POST /api/  │               │               │               │
     │   screenings ─│──────────────→│               │               │
     │               │               │               │               │
     │ Loading state │               │ StoreScreening│               │
     │ (skeleton +   │               │ Request       │               │
     │  spinner)     │               │ validation ✅  │               │
     │               │               │               │               │
     │               │               │ ═══ FASE 3: SIMPAN DATA ═══  │
     │               │               │               │               │
     │               │               │ Cek/Buat      │               │
     │               │               │ Patient record│               │
     │               │               │──────────────────────────────→│
     │               │               │               │     INSERT    │
     │               │               │               │     patients  │
     │               │               │←──────────────────────────────│
     │               │               │               │     patient_id│
     │               │               │               │               │
     │               │               │ Buat Screening│               │
     │               │               │ record        │               │
     │               │               │──────────────────────────────→│
     │               │               │               │     INSERT    │
     │               │               │               │    screenings │
     │               │               │←──────────────────────────────│
     │               │               │               │  screening_id │
     │               │               │               │               │
     │               │               │ ═══ FASE 4: PREDIKSI ML ═══  │
     │               │               │               │               │
     │               │               │ HTTP POST     │               │
     │               │               │ ml-engine:8000│               │
     │               │               │ /predict      │               │
     │               │               │ {11 features} │               │
     │               │               │──────────────→│               │q
     │               │               │               │               │
     │               │               │               │ Pydantic v2   │
     │               │               │               │ validation ✅  │
     │               │               │               │               │
     │               │               │               │ Label Encode  │
     │               │               │               │ (static map)  │
     │               │               │               │               │
     │               │               │               │ MinMax Scale  │
     │               │               │               │ (hardcoded)   │
     │               │               │               │               │
     │               │               │               │ XGBoost       │
     │               │               │               │ predict()     │
     │               │               │               │ predict_proba │
     │               │               │               │ feature_imp.  │
     │               │               │               │               │
     │               │               │  JSON response│               │
     │               │               │  {risk_level, │               │
     │               │               │   confidence, │               │
     │               │               │   features}   │               │
     │               │               │←──────────────│               │
     │               │               │               │               │
     │               │               │ ═══ FASE 5: SIMPAN HASIL ═══ │
     │               │               │               │               │
     │               │               │ Simpan        │               │
     │               │               │ Prediction    │               │
     │               │               │──────────────────────────────→│
     │               │               │               │     INSERT    │
     │               │               │               │   predictions │
     │               │               │←──────────────────────────────│
     │               │               │               │               │
     │               │               │ Log Activity  │               │
     │               │               │ (sanitized)   │               │
     │               │               │──────────────────────────────→│
     │               │               │               │     INSERT    │
     │               │               │               │ activity_logs │
     │               │               │←──────────────────────────────│
     │               │               │               │               │
     │               │               │ ═══ FASE 6: RESPONSE ═══     │
     │               │               │               │               │
     │ ScreeningResource             │               │               │
     │ + PredictionResource          │               │               │
     │←──────────────│←──────────────│               │               │
     │               │               │               │               │
     │ TanStack Query│               │               │               │
     │ onSuccess():  │               │               │               │
     │ ├── Invalidate│               │               │               │
     │ │   cache     │               │               │               │
     │ ├── Navigate  │               │               │               │
     │ │   to result │               │               │               │
     │ └── Toast ✅   │               │               │               │
     │               │               │               │               │
     │ ═══ FASE 7: VISUALISASI ═══  │               │               │
     │               │               │               │               │
     │ Render:       │               │               │               │
     │ ├── Risk Badge│               │               │               │
     │ │   (🔴🟡🟢) │               │               │               │
     │ ├── Confidence│               │               │               │
     │ │   Gauge     │               │               │               │
     │ ├── Feature   │               │               │               │
     │ │   Importance│               │               │               │
     │ │   (ECharts) │               │               │               │
     │ └── Probability               │               │               │
     │     Pie Chart │               │               │               │
     │               │               │               │               │
```

### 3.2 Waktu Respons Target

```
┌─────────────────────────────────────────────────────┐
│            RESPONSE TIME BUDGET (< 2 detik)         │
│                                                      │
│  Component              Target    Budget Share       │
│  ─────────────────────  ────────  ──────────────     │
│  Nginx routing          ~5ms     0.25%              │
│  Laravel middleware      ~30ms    1.5%              │
│  Form Request validation ~10ms    0.5%              │
│  PostgreSQL INSERT (x3)  ~50ms    2.5%              │
│  HTTP to ML Engine       ~10ms    0.5%              │
│  ML Preprocessing        ~5ms     0.25%             │
│  XGBoost Inference       ~20ms    1.0%              │
│  Feature Importance      ~5ms     0.25%             │
│  Response serialization  ~15ms    0.75%             │
│  Network overhead        ~50ms    2.5%              │
│  ─────────────────────  ────────                     │
│  TOTAL (server)          ~200ms                      │
│  Client render (ECharts) ~300ms                      │
│  ─────────────────────  ────────                     │
│  TOTAL END-TO-END        ~500ms   ✅ Well within 2s │
└─────────────────────────────────────────────────────┘
```

---

## 4. Alur ML Prediction Pipeline

### 4.1 Data Transformation Pipeline

```
RAW INPUT (dari HTTP request body)
┌──────────────────────────────────┐
│ {                                │
│   "age": 48,                     │
│   "gender": "male",             │ ← String
│   "bmi": 28.5,                  │
│   "smoking_status": "former",   │ ← String
│   "alcohol_consumption": "mod", │ ← String
│   "physical_activity": "low",   │ ← String
│   "family_history": true,       │ ← Boolean
│   "diabetes": false,            │ ← Boolean
│   "systolic_bp": 135,           │
│   "diastolic_bp": 88,           │
│   "cholesterol_level": "high"   │ ← String
│ }                                │
└──────────────┬───────────────────┘
               │
               ▼ STEP 1: PYDANTIC V2 VALIDATION
┌──────────────────────────────────┐
│ class PredictionRequest:         │
│   age: int = Field(ge=18,le=100)│
│   gender: Literal["male","fe.."]│
│   bmi: float = Field(ge=10,le60)│
│   smoking_status: Literal[...]   │
│   ... (semua 11 fields)         │
│                                  │
│ ✅ Validasi passed               │
│ ❌ 422 jika gagal                │
└──────────────┬───────────────────┘
               │
               ▼ STEP 2: LABEL ENCODING
┌──────────────────────────────────┐
│ Categorical → Numeric            │
│                                  │
│ "male"     → 0                   │
│ "former"   → 1                   │
│ "moderate" → 1                   │
│ "low"      → 0                   │
│ true       → 1                   │
│ false      → 0                   │
│ "high"     → 2                   │
│                                  │
│ Result: [48, 0, 28.5, 1, 1,     │
│          0, 1, 0, 135, 88, 2]    │
└──────────────┬───────────────────┘
               │
               ▼ STEP 3: MINMAX SCALING
┌──────────────────────────────────┐
│ X' = (X - X_min) / (X_max-X_min)│
│                                  │
│ [0.3659,  ← (48-18)/(100-18)    │
│  0.0000,  ← (0-0)/(1-0)         │
│  0.4111,  ← (28.5-10)/(55-10)   │
│  0.5000,  ← (1-0)/(2-0)         │
│  0.5000,  ← (1-0)/(2-0)         │
│  0.0000,  ← (0-0)/(2-0)         │
│  1.0000,  ← (1-0)/(1-0)         │
│  0.0000,  ← (0-0)/(1-0)         │
│  0.3611,  ← (135-70)/(250-70)   │
│  0.4364,  ← (88-40)/(150-40)    │
│  1.0000]  ← (2-0)/(2-0)         │
│                                  │
│ ⚠️ Semua nilai antara [0, 1]    │
│ ⚠️ Min/Max HARDCODED (no leak)  │
└──────────────┬───────────────────┘
               │
               ▼ STEP 4: XGBOOST INFERENCE
┌──────────────────────────────────┐
│ model = XGBClassifier(           │
│   learning_rate=0.035,           │  ← SGO-optimized
│   max_depth=9,                   │  ← SGO-optimized
│   n_estimators=285               │  ← SGO-optimized
│ )                                │
│                                  │
│ prediction = model.predict(X)    │
│ → [1]  (1 = high risk)          │
│                                  │
│ proba = model.predict_proba(X)   │
│ → [[0.08, 0.05, 0.87]]          │
│    low   med   high              │
│                                  │
│ importance =                     │
│   model.feature_importances_     │
│ → [0.156, 0.005, 0.189, ...]    │
└──────────────┬───────────────────┘
               │
               ▼ STEP 5: RESPONSE FORMATTING
┌──────────────────────────────────┐
│ {                                │
│   "risk_level": "high",         │
│   "confidence_score": 0.87,     │
│   "probability": {              │
│     "low": 0.08,                │
│     "medium": 0.05,             │
│     "high": 0.87                │
│   },                            │
│   "feature_importance": [       │
│     {"feature": "systolic_bp",  │
│      "importance": 0.234},      │
│     {"feature": "bmi",          │
│      "importance": 0.189},      │
│     ... (11 items, sorted)      │
│   ],                            │
│   "model_version": "v1.0.0-sgo",│
│   "inference_time_ms": 12       │
│ }                                │
└──────────────────────────────────┘
```

### 4.2 Mengapa Static Preprocessing?

```
┌────────────────────────────────────────────────────────────────┐
│                DATA LEAKAGE PREVENTION                        │
│                                                                │
│  ❌ WRONG (Dynamic Scaling):                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  scaler = MinMaxScaler()                               │    │
│  │  scaler.fit(new_patient_data)  ← FIT pada data BARU!   │    │
│  │  scaled = scaler.transform(new_patient_data)           │    │
│  │                                                        │    │
│  │  Masalah:                                              │    │
│  │  - Min/Max berubah setiap ada pasien baru              │    │
│  │  - Hasil prediksi BERBEDA untuk input SAMA             │    │
│  │  - Model dilatih dengan distribusi BERBEDA             │    │
│  │  - = DATA LEAKAGE                                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                │
│  ✅ CORRECT (Static Scaling):                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  # Min/Max dikunci dari distribusi TRAINING SET        │    │
│  │  FEATURE_RANGES = {                                    │    │
│  │    "age": {"min": 18, "max": 100},                    │    │
│  │    "bmi": {"min": 10.0, "max": 55.0},                │    │
│  │    ...                                                 │    │
│  │  }                                                     │    │
│  │                                                        │    │
│  │  # Formula tetap konsisten:                            │    │
│  │  scaled = (x - FIXED_MIN) / (FIXED_MAX - FIXED_MIN)  │    │
│  │                                                        │    │
│  │  Keuntungan:                                           │    │
│  │  - Input SAMA → Output SELALU SAMA                    │    │
│  │  - Konsisten dengan distribusi training                │    │
│  │  - Tidak ada data leakage                             │    │
│  │  - Deterministic & reproducible                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 5. Alur Dashboard XAI

### 5.1 Data Loading Flow

```
User navigasi ke /dashboard/xai
│
├── Vue Router: XAIDashboard.vue
│
├── TanStack Vue Query (parallel fetching):
│   ├── useStats()              → GET /api/dashboard/stats
│   ├── useRiskDistribution()   → GET /api/dashboard/risk-distribution
│   └── useFeatureImportance()  → GET /api/dashboard/feature-importance
│
├── Loading State:
│   ├── Skeleton loaders untuk setiap chart area
│   ├── Shimmer animation (pulse effect)
│   └── Progressive rendering (stat cards → charts)
│
├── Data Received:
│   ├── Stats: { total_screenings, high_risk_count, ... }
│   ├── Distribution: { low: 698, medium: 207, high: 342 }
│   └── Importance: [{ feature, importance, label }] × 11
│
└── ECharts Rendering:
    ├── Stat Cards (animated counter)
    ├── Horizontal Bar Chart (Feature Importance)
    ├── Donut Chart (Risk Distribution)
    └── Line Chart (Monthly Trend)
```

### 5.2 Chart Interactivity

```
Feature Importance Bar Chart
│
├── Hover Effect:
│   ├── Highlight bar with glow
│   ├── Show tooltip: "Tekanan Darah Sistolik: 23.4%"
│   └── Show description: "Faktor paling berpengaruh"
│
├── Click Effect:
│   ├── Filter screenings by dominant feature
│   └── Show detail breakdown
│
├── Animation:
│   ├── Bars animate from left to right on load
│   ├── Duration: 800ms (easeOutCubic)
│   └── Staggered: each bar +50ms delay
│
└── Responsive:
    ├── Desktop: Horizontal bars
    ├── Tablet: Horizontal bars (smaller)
    └── Mobile: Vertical bars
```

---

## 6. Alur RBAC & Authorization

### 6.1 Middleware Chain per Route

```
Setiap request melalui middleware chain:

GET /api/admin/users
│
├── ① ForceJsonResponse middleware
│   └── Set Accept: application/json
│
├── ② VerifyCsrfToken middleware
│   └── Cek X-XSRF-TOKEN header
│
├── ③ auth:sanctum middleware
│   ├── Cek session cookie
│   ├── Load user dari database
│   └── ❌ 401 jika tidak authenticated
│
├── ④ role:super_admin middleware
│   ├── Cek $request->user()->role
│   ├── ✅ 'super_admin' → Lanjut
│   ├── ❌ 'dokter' → 403 Forbidden
│   └── ❌ 'perawat' → 403 Forbidden
│
├── ⑤ SanitizeLogMiddleware
│   ├── Log: "User admin@... accessed admin/users"
│   └── ⚠️ TIDAK log body request/response (PHI)
│
└── ⑥ UserController@index
    └── Return UserResource::collection(User::paginate())
```

### 6.2 Permission Matrix

```
┌─────────────────────┬──────────────┬──────────┬──────────┐
│ Endpoint            │ Super Admin  │ Dokter   │ Perawat  │
├─────────────────────┼──────────────┼──────────┼──────────┤
│ POST /api/login     │      ✅      │    ✅    │    ✅    │
│ GET /api/user       │      ✅      │    ✅    │    ✅    │
│ POST /api/logout    │      ✅      │    ✅    │    ✅    │
├─────────────────────┼──────────────┼──────────┼──────────┤
│ GET /api/screenings │    ✅ all    │  ✅ all  │ ✅ own   │
│ POST /api/screenings│      ✅      │    ✅    │    ✅    │
│ GET ../prediction   │      ✅      │    ✅    │    ❌    │
├─────────────────────┼──────────────┼──────────┼──────────┤
│ GET /api/patients   │    ✅ all    │  ✅ all  │ ✅ own   │
│ POST /api/patients  │      ✅      │    ✅    │    ✅    │
├─────────────────────┼──────────────┼──────────┼──────────┤
│ GET /dashboard/*    │      ✅      │    ✅    │    ❌    │
│ GET /xai/*          │      ✅      │    ✅    │    ❌    │
├─────────────────────┼──────────────┼──────────┼──────────┤
│ GET /admin/users    │      ✅      │    ❌    │    ❌    │
│ POST /admin/users   │      ✅      │    ❌    │    ❌    │
│ PUT /admin/users/*  │      ✅      │    ❌    │    ❌    │
│ DELETE /admin/users/*│     ✅      │    ❌    │    ❌    │
│ GET /admin/audit-logs│     ✅      │    ❌    │    ❌    │
└─────────────────────┴──────────────┴──────────┴──────────┘
```

### 6.3 Frontend Route Guards

```
Vue Router Navigation Guards:

router.beforeEach((to, from, next) => {
│
├── Route requires auth? (meta.requiresAuth)
│   │
│   ├── NO → next() (public route like /login)
│   │
│   └── YES → Is user authenticated?
│       │
│       ├── NO → next('/login') + toast warning
│       │
│       └── YES → Route requires specific role? (meta.roles)
│           │
│           ├── NO → next() (any authenticated user)
│           │
│           └── YES → User has required role?
│               │
│               ├── YES → next() ✅
│               │
│               └── NO → next('/403') + toast error
│                   "Anda tidak memiliki akses ke halaman ini"
│
})
```

---

## 7. Alur Manajemen User (Admin)

```
Super Admin → /admin/users
│
├── GET /api/admin/users?page=1
│   ← UserResource::collection(paginated)
│
├── Tampilkan DataTable:
│   ┌───┬──────────────┬──────────────────┬──────────┬──────────┐
│   │ # │ Nama         │ Email            │ Role     │ Aksi     │
│   ├───┼──────────────┼──────────────────┼──────────┼──────────┤
│   │ 1 │ Dr. Siti     │ dokter@hyper.id  │ 🔵 Dokter│ ✏️ 🗑️   │
│   │ 2 │ Ns. Budi     │ perawat@hyper.id │ 🟢 Prwt │ ✏️ 🗑️   │
│   └───┴──────────────┴──────────────────┴──────────┴──────────┘
│
├── Tambah User: POST /api/admin/users
│   ├── Dialog form (nama, email, password, role)
│   ├── VeeValidate + Zod validation
│   ├── Submit → 201 Created
│   ├── TanStack Query: invalidateQueries(['users'])
│   └── Toast: "✅ User berhasil ditambahkan"
│
├── Edit User: PUT /api/admin/users/{id}
│   ├── Pre-fill form data
│   ├── Submit → 200 OK
│   └── Toast: "✅ User berhasil diperbarui"
│
└── Hapus User: DELETE /api/admin/users/{id}
    ├── Confirmation dialog
    ├── Submit → 204 No Content
    └── Toast: "✅ User berhasil dihapus"
```

---

## 8. Alur Error Handling & Recovery

### 8.1 Error Chain

```
┌───────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING CHAIN                           │
│                                                                   │
│  ML ENGINE ERROR                                                  │
│  │                                                                │
│  ├── Model not loaded → 503 ModelNotLoadedError                  │
│  ├── Invalid input → 422 ValidationError (Pydantic)              │
│  ├── Preprocessing fail → 422 PreprocessingError                 │
│  └── Unknown error → 500 InternalServerError                     │
│       │                                                           │
│       ▼                                                           │
│  BACKEND CATCH (MLEngineService.php)                             │
│  │                                                                │
│  ├── ConnectionException (ML Engine down)                        │
│  │   ├── Retry 1: wait 500ms → try again                        │
│  │   ├── Retry 2: wait 1000ms → try again                       │
│  │   ├── Retry 3: wait 2000ms → try again                       │
│  │   └── All failed → throw MLEngineException                    │
│  │                                                                │
│  ├── RequestException (timeout 30s)                              │
│  │   └── throw MLEngineException("Prediction timeout")           │
│  │                                                                │
│  ├── HTTP 422 (ML validation error)                              │
│  │   └── throw ValidationException (pass through details)        │
│  │                                                                │
│  └── HTTP 503 (Model not loaded)                                 │
│       └── throw MLEngineException("Model not ready")             │
│            │                                                      │
│            ▼                                                      │
│  LARAVEL EXCEPTION HANDLER                                       │
│  │                                                                │
│  ├── MLEngineException → 503 Service Unavailable                 │
│  │   Response: {"message": "Layanan prediksi tidak tersedia"}    │
│  │                                                                │
│  ├── ValidationException → 422 Unprocessable                     │
│  │   Response: {"message": "...", "errors": {...}}               │
│  │                                                                │
│  ├── AuthenticationException → 401 Unauthorized                  │
│  │   Response: {"message": "Unauthenticated"}                   │
│  │                                                                │
│  └── AuthorizationException → 403 Forbidden                     │
│       Response: {"message": "Forbidden"}                         │
│            │                                                      │
│            ▼                                                      │
│  FRONTEND HANDLING (Axios interceptor)                           │
│  │                                                                │
│  ├── 401 → Redirect to /login + clear authStore                 │
│  ├── 403 → Toast error: "Akses ditolak"                         │
│  ├── 422 → Show validation errors on form fields                │
│  ├── 503 → Toast error: "Layanan sedang tidak tersedia"         │
│  │         + Show retry button                                   │
│  └── 500 → Toast error: "Terjadi kesalahan server"              │
│            + Log to console for debugging                        │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 8.2 Circuit Breaker Pattern (Future Enhancement)

```
Normal State
    │
    ▼
3 consecutive failures
    │
    ▼
Open State (reject all requests for 30s)
    │
    ▼ after 30s
Half-Open State (allow 1 test request)
    │
    ├── Success → Normal State ✅
    └── Failure → Open State 🔴
```

---

## 9. Alur Data Persistence

### 9.1 Database Write Flow

```
Skrining baru disubmit:

┌───────────────────────────────────────────────────────────────┐
│ TRANSACTION (atomic - all or nothing)                        │
│                                                               │
│  ① INSERT INTO patients (name, nik, dob, gender, ...)       │
│     → patient_id = 42                                        │
│                                                               │
│  ② INSERT INTO screenings (patient_id, user_id, age, ...)   │
│     → screening_id = 127                                     │
│                                                               │
│  ③ [HTTP Call to ML Engine - outside transaction]            │
│     → prediction result                                      │
│                                                               │
│  ④ INSERT INTO predictions (screening_id, risk_level, ...)   │
│     → prediction_id = 127                                    │
│                                                               │
│  ⑤ INSERT INTO activity_logs (user_id, action, ...)         │
│     → log_id = 543                                           │
│     → description: "User #3 created screening #127"          │
│     → ⚠️ NO patient name, NO medical data in log!           │
│                                                               │
│  COMMIT ✅                                                    │
│                                                               │
│  Jika step ①-② gagal → ROLLBACK semua                       │
│  Jika step ③ gagal → ROLLBACK + return error                │
│  Jika step ④-⑤ gagal → ROLLBACK semua                       │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 9.2 Activity Log Sanitization

```
┌─────────────────────────────────────────────────────┐
│           AUDIT LOG SANITIZATION                    │
│                                                      │
│  WHAT WE LOG:                                        │
│  ✅ User ID (siapa yang melakukan)                   │
│  ✅ Action type ("screening.created")                │
│  ✅ Entity type ("App\Models\Screening")             │
│  ✅ Entity ID (127)                                  │
│  ✅ Timestamp (2024-11-15T10:30:00Z)                │
│  ✅ IP Address (192.168.1.100)                       │
│  ✅ User Agent (Chrome/120...)                       │
│  ✅ Generic description ("Created screening #127")   │
│                                                      │
│  WHAT WE NEVER LOG:                                  │
│  ❌ Patient name                                     │
│  ❌ NIK (National ID)                                │
│  ❌ Medical data (BP, BMI, etc.)                     │
│  ❌ Prediction results                               │
│  ❌ Request/Response bodies                          │
│  ❌ Any PHI (Protected Health Information)            │
│                                                      │
│  Contoh log entry:                                   │
│  {                                                   │
│    "user_id": 3,                                     │
│    "action": "screening.created",                    │
│    "entity_type": "Screening",                       │
│    "entity_id": 127,                                 │
│    "description": "User created a new screening",   │
│    "ip_address": "192.168.1.100",                    │
│    "created_at": "2024-11-15 10:30:00"              │
│  }                                                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 10. Alur Dark/Light Mode

```
┌─────────────────────────────────────────────────────────┐
│                    THEME FLOW                           │
│                                                          │
│  App.vue (mounted):                                      │
│  │                                                       │
│  ├── Check localStorage('theme')                        │
│  │   ├── 'dark' → Set document.class = 'dark'          │
│  │   ├── 'light' → Remove 'dark' class                 │
│  │   └── null → Check system preference                │
│  │       ├── prefers-color-scheme: dark → 'dark'       │
│  │       └── prefers-color-scheme: light → 'light'     │
│  │                                                       │
│  ▼                                                       │
│  themeStore (Pinia):                                     │
│  ├── state: { isDark: boolean }                         │
│  ├── action: toggleTheme()                              │
│  │   ├── isDark = !isDark                               │
│  │   ├── document.documentElement.classList.toggle('dark')│
│  │   └── localStorage.setItem('theme', isDark?'dark':'light')│
│  │                                                       │
│  ▼                                                       │
│  CSS Variables (globals.css):                            │
│  │                                                       │
│  │  :root {                                              │
│  │    --background: 0 0% 100%;        /* White */       │
│  │    --foreground: 222.2 84% 4.9%;   /* Near black */  │
│  │    --card: 0 0% 100%;                                │
│  │    --primary: 173 58% 39%;         /* Medical teal */│
│  │    --primary-foreground: 0 0% 100%;                  │
│  │    --muted: 210 40% 96%;                             │
│  │    --border: 214 32% 91%;                            │
│  │    --ring: 173 58% 39%;                              │
│  │    ...                                                │
│  │  }                                                    │
│  │                                                       │
│  │  .dark {                                              │
│  │    --background: 222.2 84% 4.9%;   /* Near black */  │
│  │    --foreground: 210 40% 98%;      /* Near white */  │
│  │    --card: 222.2 84% 6%;                             │
│  │    --primary: 173 58% 45%;         /* Lighter teal */│
│  │    --primary-foreground: 0 0% 100%;                  │
│  │    --muted: 217 33% 17%;                             │
│  │    --border: 217 33% 17%;                            │
│  │    --ring: 173 58% 45%;                              │
│  │    ...                                                │
│  │  }                                                    │
│  │                                                       │
│  ▼                                                       │
│  ThemeToggle.vue:                                        │
│  ├── Button with Sun/Moon icon                          │
│  ├── Click → themeStore.toggleTheme()                   │
│  ├── Icon rotation animation (180°, 300ms)              │
│  └── Smooth CSS transition on all theme-aware elements  │
│      transition: background-color 200ms, color 200ms    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Ringkasan Semua Alur

| # | Alur | Trigger | Services Terlibat | Output |
|---|------|---------|-------------------|--------|
| 1 | Startup | `docker compose up` | All 5 services | Sistem ready |
| 2 | Login | User submit form | Frontend → Nginx → Backend → DB | Session cookie |
| 3 | Skrining | User submit skrining | All 5 services | Prediksi risiko |
| 4 | ML Pipeline | Backend call ML | ML Engine → XGBoost | Risk + Features |
| 5 | Dashboard XAI | User buka dashboard | Frontend → Backend → DB | Charts & stats |
| 6 | RBAC | Setiap API request | Backend middleware | Allow/Deny |
| 7 | User Mgmt | Admin CRUD user | Frontend → Backend → DB | User updated |
| 8 | Error Handling | Any failure | All services | Graceful recovery |
| 9 | Data Persist | CRUD operations | Backend → PostgreSQL | Data stored |
| 10 | Theme Toggle | User click toggle | Frontend only | UI theme change |
| 11 | Ekspor PDF | User klik "Unduh PDF" | Frontend (html2pdf.js) | File PDF |
| 12 | Audit Logging | Modifikasi data | Backend (ActivityLogService) | Jejak terekam |

---

## 11. Alur Ekspor Laporan PDF (Client-Side)

### Sequence Diagram Detail

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│   User   │    │  Vue.js  │    │html2pdf.js│
│ Browser  │    │ Frontend │    │  Library  │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     │ Klik "Unduh   │               │
     │ Laporan PDF"  │               │
     │──────────────→│               │
     │               │ Target div    │
     │               │ #pdf-content  │
     │               │──────────────→│
     │               │               │ Generate
     │               │               │ Canvas
     │               │←──────────────│
     │               │               │
     │ Download File │               │
     │ .pdf          │               │
     │←──────────────│               │
```

**Penjelasan:**
- Menggunakan strategi *Client-Side Generation* untuk membebaskan beban Server (Laravel/PHP).
- Rendering dilakukan melalui Canvas yang langsung dicetak menjadi lembar A4.

---

<p align="center">
  <strong>Dokumentasi Alur Sistem v1.0</strong><br>
  Sistem Deteksi Dini Risiko Hipertensi<br>
  Built with ❤️ for better healthcare
</p>
