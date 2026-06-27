# 📖 WALKTHROUGH - Panduan Lengkap Sistem Deteksi Dini Risiko Hipertensi

> Dokumen ini berisi panduan langkah-demi-langkah (walkthrough) untuk memahami, menginstal, mengkonfigurasi, dan menggunakan Sistem Deteksi Dini Risiko Hipertensi dari nol hingga production-ready.

---

## Daftar Isi Walkthrough

1. [Fase 1: Pemahaman Arsitektur](#fase-1-pemahaman-arsitektur)
2. [Fase 2: Setup Environment](#fase-2-setup-environment)
3. [Fase 3: Build Infrastructure (Docker)](#fase-3-build-infrastructure-docker)
4. [Fase 4: Backend Laravel — API Gateway](#fase-4-backend-laravel--api-gateway)
5. [Fase 5: ML Engine — FastAPI & XGBoost](#fase-5-ml-engine--fastapi--xgboost)
6. [Fase 6: Frontend Vue.js — SPA Klinis](#fase-6-frontend-vuejs--spa-klinis)
7. [Fase 7: Integrasi End-to-End](#fase-7-integrasi-end-to-end)
8. [Fase 8: Testing & Quality Assurance](#fase-8-testing--quality-assurance)
9. [Fase 9: Deployment Production](#fase-9-deployment-production)
10. [Fase 10: Monitoring & Maintenance](#fase-10-monitoring--maintenance)

---

## 🚧 Status Pengembangan (Progress Checklist)
- [x] **Fase Perencanaan**: Pembuatan README, WALKTHROUGH, dan ALUR SISTEM.
- [x] **Fase 1**: Pemahaman Arsitektur (Selesai secara konsep).
- [x] **Fase 2**: Setup Environment.
- [x] **Fase 3**: Build Infrastructure (Docker).
- [x] **Fase 4**: Backend Laravel — API Gateway.
- [x] **Fase 5**: ML Engine — FastAPI & XGBoost.
- [x] **Fase 6**: Frontend Vue.js — SPA Klinis.
- [x] **Fase Khusus**: Refaktor UI/UX HealthTech Enterprise.
- [x] **Fase 7**: Integrasi End-to-End.
- [x] **Fase 8**: Testing & Quality Assurance.
- [x] **Fase 9**: Deployment Production.
- [x] **Fase 10**: Monitoring & Maintenance.

---

## Fase 1: Pemahaman Arsitektur

### 1.1 Konsep Dasar Microservices

Sistem ini menggunakan **4 microservices** yang saling terisolasi namun berkomunikasi melalui jaringan Docker internal:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARSITEKTUR MICROSERVICES                     │
│                                                                 │
│  Service 1: NGINX (Reverse Proxy + SSL)                        │
│  ├── Fungsi: Routing, load balancing, SSL termination           │
│  ├── Port: 80 (HTTP→redirect), 443 (HTTPS)                     │
│  └── Network: hyper_public_net                                  │
│                                                                 │
│  Service 2: FRONTEND (Vue.js 3 SPA)                            │
│  ├── Fungsi: User interface, form skrining, dashboard           │
│  ├── Port: 5173 (dev) / served by nginx (prod)                 │
│  └── Network: hyper_public_net                                  │
│                                                                 │
│  Service 3: BACKEND (Laravel 11 API)                           │
│  ├── Fungsi: API Gateway, Auth, RBAC, Orchestration            │
│  ├── Port: 9000 (PHP-FPM internal)                             │
│  └── Network: hyper_public_net + hyper_internal_net             │
│                                                                 │
│  Service 4: ML ENGINE (FastAPI + XGBoost)                      │
│  ├── Fungsi: Prediction, preprocessing, feature importance      │
│  ├── Port: 8000 (internal only)                                │
│  └── Network: hyper_internal_net                                │
│                                                                 │
│  Service 5: POSTGRESQL 15 (Database)                           │
│  ├── Fungsi: Persistent data storage                           │
│  ├── Port: 5432 (internal only)                                │
│  └── Network: hyper_internal_net                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Mengapa Arsitektur Ini?

| Pertanyaan | Jawaban |
|------------|---------|
| Mengapa microservices? | Setiap komponen bisa di-scale, di-update, dan di-deploy secara independen |
| Mengapa 2 zona jaringan? | Database dan ML Engine tidak boleh diakses dari internet — defense in depth |
| Mengapa Nginx di depan? | SSL termination terpusat, security headers, dan caching |
| Mengapa Laravel sebagai gateway? | Mengorkestrasi auth, validasi, logging, dan komunikasi antar service |
| Mengapa FastAPI terpisah? | Python ML ecosystem (XGBoost, NumPy) lebih efisien dijalankan terpisah |
| Mengapa static preprocessing? | Mencegah data leakage — parameter scaling dikunci dari training set |

### 1.3 Alur Data End-to-End

```
USER (Browser)
    │
    │ 1. HTTPS Request
    ▼
NGINX (:443)
    │
    │ 2. SSL Termination + Routing
    ├─── GET /* ──────────→ Frontend (Vue.js SPA)
    │                       ├── Render UI
    │                       ├── State Management (Pinia)
    │                       └── API Calls (Axios + TanStack Query)
    │
    ├─── POST /api/* ────→ Backend (Laravel 11)
    │                       ├── CSRF + Sanctum Auth Check
    │                       ├── RBAC Middleware Check
    │                       ├── Form Request Validation
    │                       ├── Business Logic
    │                       ├── PostgreSQL CRUD
    │                       ├── Activity Logging (sanitized)
    │                       │
    │                       │ 3. Internal HTTP Call
    │                       └──→ ML Engine (FastAPI)
    │                             ├── Pydantic v2 Validation
    │                             ├── Label Encoding (static)
    │                             ├── MinMax Scaling (static)
    │                             ├── XGBoost Prediction
    │                             ├── Feature Importance
    │                             └── Return JSON Response
    │
    │ 4. JSON Response
    ▼
USER (Browser) ── Visualize Result (ECharts Dashboard)
```

---

## Fase 2: Setup Environment

### 2.1 Install Docker Desktop

#### Windows (WSL2)
```powershell
# 1. Enable WSL2
wsl --install

# 2. Download Docker Desktop dari https://www.docker.com/products/docker-desktop
# 3. Install dan restart komputer
# 4. Verifikasi instalasi
docker --version           # Docker version 24.0+
docker compose version     # Docker Compose version v2.20+
```

#### macOS
```bash
# Menggunakan Homebrew
brew install --cask docker

# Atau download dari https://www.docker.com/products/docker-desktop
```

#### Linux (Ubuntu/Debian)
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose Plugin
sudo apt-get install docker-compose-plugin

# Add user ke docker group
sudo usermod -aG docker $USER
```

### 2.2 Clone & Setup Project

```bash
# Clone repository
git clone https://github.com/your-org/hypertension-detection-system.git
cd hypertension-detection-system

# Buat file environment dari template
cp .env.example .env

# Buat SSL certificate self-signed (development only)
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/self-signed.key \
  -out nginx/ssl/self-signed.crt \
  -subj "/C=ID/ST=DKI Jakarta/L=Jakarta/O=HealthTech/CN=localhost"
```

### 2.3 Struktur `.env` yang Harus Diisi

```env
# File: .env (root project)

# ── APPLICATION ──────────────────────────────────
APP_NAME="Sistem Deteksi Dini Risiko Hipertensi"
APP_ENV=local                     # Options: local, staging, production
APP_DEBUG=true                    # Set false di production!

# ── DATABASE ─────────────────────────────────────
DB_CONNECTION=pgsql
DB_HOST=postgres                  # Nama service di docker-compose
DB_PORT=5432
DB_DATABASE=hypertension_db
DB_USERNAME=hyper_admin
DB_PASSWORD=your_secure_password  # ⚠️ GANTI ini!

# ── ML ENGINE ────────────────────────────────────
ML_ENGINE_HOST=ml-engine          # Nama service di docker-compose
ML_ENGINE_PORT=8000
ML_ENGINE_TIMEOUT=30              # Timeout dalam detik
ML_ENGINE_RETRY_TIMES=3           # Jumlah retry
ML_ENGINE_RETRY_SLEEP=500         # Delay antar retry (ms)

# ── NGINX ────────────────────────────────────────
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
```

---

## Fase 3: Build Infrastructure (Docker)

### 3.1 docker-compose.yml — Penjelasan Lengkap

```yaml
# docker-compose.yml
# Orkestrasi 5 services dengan isolasi jaringan tingkat tinggi

version: "3.9"

# ═══════════════════════════════════════════════
# SERVICES
# ═══════════════════════════════════════════════
services:

  # ─── NGINX REVERSE PROXY ───────────────────
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: hyper_nginx
    ports:
      - "${NGINX_HTTP_PORT:-80}:80"
      - "${NGINX_HTTPS_PORT:-443}:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/snippets:/etc/nginx/snippets:ro
      - frontend_dist:/usr/share/nginx/html:ro  # Production: serve built frontend
    depends_on:
      backend:
        condition: service_healthy
      frontend:
        condition: service_started
    networks:
      - hyper_public_net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ─── FRONTEND (Vue.js 3) ──────────────────
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development          # Multi-stage: development | production
    container_name: hyper_frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules           # Anonymous volume untuk node_modules
    environment:
      - VITE_API_BASE_URL=https://localhost/api
      - VITE_APP_NAME=${APP_NAME}
    networks:
      - hyper_public_net
    restart: unless-stopped

  # ─── BACKEND (Laravel 11) ─────────────────
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    container_name: hyper_backend
    volumes:
      - ./backend:/var/www/html
      - /var/www/html/vendor        # Anonymous volume untuk vendor
    env_file:
      - ./backend/.env
    depends_on:
      postgres:
        condition: service_healthy
      ml-engine:
        condition: service_healthy
    networks:
      - hyper_public_net             # ← Dapat diakses oleh Nginx
      - hyper_internal_net           # ← Dapat mengakses ML Engine & DB
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "php", "artisan", "health:check"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # ─── ML ENGINE (FastAPI + XGBoost) ────────
  ml-engine:
    build:
      context: ./ml-engine
      dockerfile: Dockerfile
    container_name: hyper_ml_engine
    volumes:
      - ./ml-engine:/app
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
      - MODEL_PATH=/app/artifacts/xgboost_sgo_model.json
      - LOG_LEVEL=info
    networks:
      - hyper_internal_net           # ← HANYA jaringan internal
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ─── POSTGRESQL 15 ────────────────────────
  postgres:
    image: postgres:15-alpine
    container_name: hyper_postgres
    environment:
      POSTGRES_DB: ${DB_DATABASE:-hypertension_db}
      POSTGRES_USER: ${DB_USERNAME:-hyper_admin}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - hyper_pgdata:/var/lib/postgresql/data  # Persistent volume
    networks:
      - hyper_internal_net           # ← HANYA jaringan internal
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USERNAME:-hyper_admin} -d ${DB_DATABASE:-hypertension_db}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

# ═══════════════════════════════════════════════
# NETWORKS (Isolasi Zona)
# ═══════════════════════════════════════════════
networks:
  hyper_public_net:
    driver: bridge
    name: hyper_public_net
    ipam:
      config:
        - subnet: 172.20.0.0/24     # Subnet zona publik

  hyper_internal_net:
    driver: bridge
    name: hyper_internal_net
    internal: true                   # ⛔ NO INTERNET ACCESS
    ipam:
      config:
        - subnet: 172.21.0.0/24     # Subnet zona internal

# ═══════════════════════════════════════════════
# VOLUMES (Persistent Storage)
# ═══════════════════════════════════════════════
volumes:
  hyper_pgdata:
    driver: local
    name: hyper_pgdata
  frontend_dist:
    driver: local
    name: hyper_frontend_dist
```

### 3.2 Dockerfiles — Multi-Stage Build

#### Nginx Dockerfile
```dockerfile
# nginx/Dockerfile
FROM nginx:1.25-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/
COPY snippets/ /etc/nginx/snippets/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD nginx -t || exit 1

EXPOSE 80 443
```

#### Frontend Dockerfile (Multi-Stage)
```dockerfile
# frontend/Dockerfile
# ═══ Stage 1: Development ═══
FROM node:20-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ═══ Stage 2: Build ═══
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ═══ Stage 3: Production ═══
FROM nginx:1.25-alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Backend Dockerfile (Multi-Stage)
```dockerfile
# backend/Dockerfile
# ═══ Stage 1: Development ═══
FROM php:8.2-fpm-alpine AS development

# Install system dependencies
RUN apk add --no-cache \
    postgresql-dev \
    libzip-dev \
    oniguruma-dev \
    curl \
    && docker-php-ext-install pdo_pgsql pgsql zip mbstring bcmath opcache

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html
COPY composer.json composer.lock ./
RUN composer install --no-scripts --no-autoloader
COPY . .
RUN composer dump-autoload --optimize

# PHP-FPM config
RUN cp /usr/local/etc/php/php.ini-development /usr/local/etc/php/php.ini

EXPOSE 9000
CMD ["php-fpm"]

# ═══ Stage 2: Production ═══
FROM php:8.2-fpm-alpine AS production

RUN apk add --no-cache \
    postgresql-dev \
    libzip-dev \
    oniguruma-dev \
    && docker-php-ext-install pdo_pgsql pgsql zip mbstring bcmath opcache

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --optimize-autoloader
COPY . .
RUN composer dump-autoload --optimize

# PHP production settings
RUN cp /usr/local/etc/php/php.ini-production /usr/local/etc/php/php.ini
COPY docker/php/opcache.ini /usr/local/etc/php/conf.d/opcache.ini

# Set permissions
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

EXPOSE 9000
CMD ["php-fpm"]
```

#### ML Engine Dockerfile (Multi-Stage)
```dockerfile
# ml-engine/Dockerfile
# ═══ Stage 1: Builder ═══
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ═══ Stage 2: Runtime ═══
FROM python:3.10-slim AS runtime
WORKDIR /app

# Copy installed packages
COPY --from=builder /install /usr/local

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' mluser && chown -R mluser:mluser /app
USER mluser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### 3.3 Build & Run

```bash
# Build semua images
docker compose build

# Start semua services (detached mode)
docker compose up -d

# Cek status
docker compose ps

# Expected output:
# NAME              STATUS              PORTS
# hyper_nginx       running             0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
# hyper_frontend    running             5173/tcp
# hyper_backend     running (healthy)   9000/tcp
# hyper_ml_engine   running (healthy)   8000/tcp
# hyper_postgres    running (healthy)   5432/tcp
```

### 3.4 Verifikasi Jaringan Isolasi

```bash
# Verifikasi nginx TIDAK bisa akses ml-engine
docker compose exec nginx ping ml-engine
# Expected: ping: bad address 'ml-engine' (TIDAK BISA RESOLVE)

# Verifikasi backend BISA akses ml-engine
docker compose exec backend curl http://ml-engine:8000/health
# Expected: {"status": "healthy", "model_loaded": true}

# Verifikasi ml-engine TIDAK bisa akses internet
docker compose exec ml-engine curl -s --connect-timeout 5 https://google.com
# Expected: Connection timed out (BLOCKED)
```

---

## Fase 4: Backend Laravel — API Gateway

### 4.1 Initial Setup

```bash
# Masuk ke container backend
docker compose exec backend sh

# Generate application key
php artisan key:generate

# Jalankan migrasi database
php artisan migrate

# Jalankan seeder (buat default users)
php artisan db:seed

# Clear caches
php artisan config:clear
php artisan cache:clear
```

### 4.2 Default Users (Setelah Seeding)

| Role | Email | Password | Deskripsi |
|------|-------|----------|-----------|
| Super Admin | `admin@hypertension.id` | `password` | Full access |
| Dokter | `dokter@hypertension.id` | `password` | Clinical access |
| Perawat | `perawat@hypertension.id` | `password` | Basic screening |

> ⚠️ **PENTING:** Ganti password default ini segera setelah deployment!

### 4.3 Key Backend Files — Penjelasan

#### `app/Services/MLEngineService.php`
```
Fungsi: Berkomunikasi dengan ML Engine via HTTP
├── predict($data) ─── POST ke http://ml-engine:8000/predict
│   ├── Timeout: 30 detik (configurable)
│   ├── Retry: 3x dengan exponential backoff
│   └── Exception handling: MLEngineException
├── health() ─── GET ke http://ml-engine:8000/health
└── Konfigurasi dibaca dari config/services.php
```

#### `app/Http/Middleware/RoleMiddleware.php`
```
Fungsi: Enforce RBAC pada route-level
├── Route::middleware('role:super_admin') ─── Hanya admin
├── Route::middleware('role:dokter') ─── Dokter + Admin
├── Route::middleware('role:perawat') ─── Semua role
└── Return 403 jika role tidak match
```

#### `app/Http/Requests/StoreScreeningRequest.php`
```
Fungsi: Validasi 11 atribut sebelum masuk ke controller
├── age ─── required|integer|min:18|max:100
├── gender ─── required|in:male,female
├── bmi ─── required|numeric|min:10|max:60
├── smoking_status ─── required|in:never,former,current
├── alcohol_consumption ─── required|in:none,moderate,heavy
├── physical_activity ─── required|in:low,moderate,high
├── family_history ─── required|boolean
├── diabetes ─── required|boolean
├── systolic_bp ─── required|integer|min:70|max:250
├── diastolic_bp ─── required|integer|min:40|max:150
└── cholesterol_level ─── required|in:normal,borderline,high
```

### 4.4 Route Map

```php
// routes/api.php

// ── PUBLIC ROUTES ───────────────────────
Route::post('/login', [LoginController::class, 'store']);
Route::get('/health', [HealthCheckController::class, 'index']);

// ── AUTHENTICATED ROUTES (Sanctum) ─────
Route::middleware('auth:sanctum')->group(function () {

    // User Profile
    Route::get('/user', [ProfileController::class, 'show']);
    Route::post('/logout', [LogoutController::class, 'destroy']);

    // Screening (Dokter + Perawat)
    Route::apiResource('screenings', ScreeningController::class);
    Route::get('/screenings/{screening}/prediction', [ScreeningController::class, 'prediction']);

    // Patients
    Route::apiResource('patients', PatientController::class);
    Route::get('/patients/{patient}/screenings', [PatientController::class, 'screenings']);

    // Dashboard (Dokter + Admin)
    Route::middleware('role:dokter')->prefix('dashboard')->group(function () {
        Route::get('/stats', [DashboardController::class, 'stats']);
        Route::get('/risk-distribution', [DashboardController::class, 'riskDistribution']);
        Route::get('/feature-importance', [DashboardController::class, 'featureImportance']);
    });

    // Admin Only
    Route::middleware('role:super_admin')->prefix('admin')->group(function () {
        Route::apiResource('users', UserController::class);
        Route::get('/audit-logs', [AuditLogController::class, 'index']);
    });
});
```

---

## Fase 5: ML Engine — FastAPI & XGBoost

### 5.1 Struktur ML Engine

```
ml-engine/
├── app/
│   ├── main.py                 # FastAPI app dengan lifespan
│   ├── config.py               # Settings class
│   ├── api/
│   │   └── routes.py           # /predict, /health endpoints
│   ├── core/
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── middleware.py       # Request logging, timing
│   ├── models/
│   │   └── xgboost_model.py   # Model loader & predictor
│   ├── pipeline/
│   │   ├── preprocessor.py    # Orchestrate encoding + scaling
│   │   ├── label_encoder.py   # Static categorical encoding
│   │   └── scaler.py          # Static MinMax scaling
│   └── schemas/
│       ├── request.py          # Pydantic v2 input schema
│       └── response.py        # Pydantic v2 output schema
├── artifacts/
│   └── xgboost_sgo_model.json # Trained model file
├── requirements.txt
└── tests/
```

### 5.2 Pipeline Preprocessing — Step-by-Step

```
Input Data (dari Laravel Backend)
│
│  {
│    "age": 48,
│    "gender": "male",
│    "bmi": 28.5,
│    "smoking_status": "former",
│    "alcohol_consumption": "moderate",
│    "physical_activity": "low",
│    "family_history": true,
│    "diabetes": false,
│    "systolic_bp": 135,
│    "diastolic_bp": 88,
│    "cholesterol_level": "high"
│  }
│
▼ Step 1: Pydantic v2 Validation
│  ✅ Validasi tipe data
│  ✅ Validasi range (age: 18-100, bmi: 10-60, dst.)
│  ✅ Validasi enum values
│
▼ Step 2: Label Encoding (Static Map)
│  gender: "male" → 0
│  smoking_status: "former" → 1
│  alcohol_consumption: "moderate" → 1
│  physical_activity: "low" → 0
│  family_history: true → 1
│  diabetes: false → 0
│  cholesterol_level: "high" → 2
│
│  Hasil: [48, 0, 28.5, 1, 1, 0, 1, 0, 135, 88, 2]
│
▼ Step 3: MinMax Scaling (Static — Hardcoded)
│  Formula: X_scaled = (X - X_min) / (X_max - X_min)
│
│  age:         (48 - 18) / (100 - 18)  = 0.3659
│  gender:      (0 - 0) / (1 - 0)       = 0.0000
│  bmi:         (28.5 - 10) / (55 - 10)  = 0.4111
│  smoking:     (1 - 0) / (2 - 0)       = 0.5000
│  alcohol:     (1 - 0) / (2 - 0)       = 0.5000
│  activity:    (0 - 0) / (2 - 0)       = 0.0000
│  family:      (1 - 0) / (1 - 0)       = 1.0000
│  diabetes:    (0 - 0) / (1 - 0)       = 0.0000
│  systolic:    (135 - 70) / (250 - 70)  = 0.3611
│  diastolic:   (88 - 40) / (150 - 40)   = 0.4364
│  cholesterol: (2 - 0) / (2 - 0)       = 1.0000
│
│  Hasil: [0.3659, 0.0, 0.4111, 0.5, 0.5, 0.0, 1.0, 0.0, 0.3611, 0.4364, 1.0]
│
▼ Step 4: XGBoost Prediction
│  model.predict_proba(X) → [0.08, 0.05, 0.87]  (low, medium, high)
│  model.predict(X) → 1 (high risk)
│
▼ Step 5: Feature Importance Extraction
│  model.feature_importances_ → [0.156, 0.005, 0.189, 0.045, 0.012, 0.067, 0.134, 0.022, 0.234, 0.038, 0.098]
│  Sorted descending, labeled with feature names
│
▼ Output Response
│  {
│    "risk_level": "high",
│    "confidence_score": 0.87,
│    "probability": {"low": 0.08, "medium": 0.05, "high": 0.87},
│    "feature_importance": [
│      {"feature": "systolic_bp", "importance": 0.234},
│      {"feature": "bmi", "importance": 0.189},
│      ...
│    ],
│    "model_version": "v1.0.0-sgo",
│    "inference_time_ms": 12
│  }
```

### 5.3 Key Code: main.py

```python
# ml-engine/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.xgboost_model import XGBoostPredictor
from app.api.routes import router
from app.core.middleware import RequestTimingMiddleware
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Global model instance
model_predictor: XGBoostPredictor | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, cleanup on shutdown."""
    global model_predictor
    logger.info("🚀 Loading XGBoost model...")
    model_predictor = XGBoostPredictor(settings.MODEL_PATH)
    model_predictor.load()
    logger.info(f"✅ Model loaded successfully (version: {model_predictor.version})")
    yield
    logger.info("👋 Shutting down ML Engine...")
    model_predictor = None

app = FastAPI(
    title="Hypertension Risk Detection ML Engine",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,       # Disable docs (internal service)
    redoc_url=None,
)

app.add_middleware(RequestTimingMiddleware)
app.include_router(router)
```

### 5.4 Key Code: Prediction Endpoint

```python
# ml-engine/app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse, HealthResponse
from app.pipeline.preprocessor import Preprocessor
from app.core.exceptions import ModelNotLoadedError, PreprocessingError
import time

router = APIRouter()
preprocessor = Preprocessor()

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Run hypertension risk prediction pipeline."""
    start_time = time.perf_counter()
    
    try:
        # Step 1: Preprocess (label encode + MinMax scale)
        features = preprocessor.transform(request)
        
        # Step 2: Predict
        from app.main import model_predictor
        if model_predictor is None:
            raise ModelNotLoadedError()
        
        prediction = model_predictor.predict(features)
        probabilities = model_predictor.predict_proba(features)
        feature_importance = model_predictor.get_feature_importance()
        
        # Step 3: Build response
        inference_time = int((time.perf_counter() - start_time) * 1000)
        
        return PredictionResponse(
            risk_level=prediction,
            confidence_score=max(probabilities),
            probability={
                "low": probabilities[0],
                "medium": probabilities[1] if len(probabilities) > 2 else 0,
                "high": probabilities[-1],
            },
            feature_importance=feature_importance,
            model_version=model_predictor.version,
            inference_time_ms=inference_time,
        )
    except PreprocessingError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ModelNotLoadedError:
        raise HTTPException(status_code=503, detail="Model not loaded")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    from app.main import model_predictor
    return HealthResponse(
        status="healthy",
        model_loaded=model_predictor is not None,
        model_version=model_predictor.version if model_predictor else None,
    )
```

---

## Fase 6: Frontend Vue.js — SPA Klinis

### 6.1 Project Setup

```bash
# Di dalam container frontend atau lokal
npm create vite@latest . -- --template vue-ts

# Install core dependencies
npm install vue-router@4 pinia @tanstack/vue-query axios
npm install vee-validate @vee-validate/zod zod
npm install echarts vue-echarts

# Install UI dependencies
npm install tailwindcss postcss autoprefixer
npm install -D @types/node
npx tailwindcss init -p

# Install Shadcn Vue (manual setup)
npm install radix-vue class-variance-authority clsx tailwind-merge
npm install lucide-vue-next
```

### 6.2 State Management Architecture

```
┌────────────────────────────────────────────────────────┐
│                 STATE MANAGEMENT                       │
│                                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              PINIA STORES                       │   │
│  │  (Client State — Synchronous)                   │   │
│  │                                                 │   │
│  │  authStore.ts                                   │   │
│  │  ├── user: User | null                          │   │
│  │  ├── isAuthenticated: boolean                   │   │
│  │  ├── role: 'super_admin' | 'dokter' | 'perawat' │   │
│  │  └── actions: login(), logout(), fetchUser()    │   │
│  │                                                 │   │
│  │  themeStore.ts                                  │   │
│  │  ├── isDark: boolean                            │   │
│  │  └── actions: toggleTheme()                     │   │
│  │                                                 │   │
│  │  screeningStore.ts                              │   │
│  │  ├── currentStep: number (1-4)                  │   │
│  │  ├── formData: Partial<ScreeningData>           │   │
│  │  └── actions: nextStep(), prevStep(), reset()   │   │
│  │                                                 │   │
│  │  uiStore.ts                                     │   │
│  │  ├── isSidebarOpen: boolean                     │   │
│  │  ├── isLoading: boolean                         │   │
│  │  └── actions: toggleSidebar(), setLoading()     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │          TANSTACK VUE QUERY                     │   │
│  │  (Server State — Asynchronous + Caching)        │   │
│  │                                                 │   │
│  │  useScreeningQueries.ts                         │   │
│  │  ├── useScreenings() → GET /api/screenings      │   │
│  │  ├── useScreening(id) → GET /api/screenings/:id │   │
│  │  ├── useCreateScreening() → POST mutation       │   │
│  │  └── Cache: staleTime 5min, gcTime 10min        │   │
│  │                                                 │   │
│  │  useDashboardQueries.ts                         │   │
│  │  ├── useStats() → GET /api/dashboard/stats      │   │
│  │  ├── useRiskDistribution()                      │   │
│  │  └── useFeatureImportance()                     │   │
│  │                                                 │   │
│  │  usePatientQueries.ts                           │   │
│  │  ├── usePatients(filters)                       │   │
│  │  └── usePatient(id)                             │   │
│  └─────────────────────────────────────────────────┘   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 6.3 Multi-Step Form — Alur User

```
LANGKAH 1: Identitas Pasien
┌─────────────────────────────────────┐
│  ● ○ ○ ○  Step 1 of 4              │
│                                     │
│  Nama Lengkap: [________________]   │
│  NIK:          [________________]   │
│  Tanggal Lahir: [__/__/____]        │
│  Jenis Kelamin: [▼ Pilih...]        │
│  Usia:          [auto-calculated]   │
│                                     │
│              [Selanjutnya →]        │
└─────────────────────────────────────┘
         │ Zod validasi semua field
         ▼
LANGKAH 2: Riwayat Medis
┌─────────────────────────────────────┐
│  ● ● ○ ○  Step 2 of 4              │
│                                     │
│  Tekanan Darah Sistolik: [___] mmHg │
│  Tekanan Darah Diastolik: [___] mmHg│
│  BMI (Indeks Massa Tubuh): [____]   │
│  Riwayat Keluarga: [○ Ya  ○ Tidak]  │
│  Riwayat Diabetes: [○ Ya  ○ Tidak]  │
│  Kadar Kolesterol: [▼ Pilih...]     │
│                                     │
│  [← Kembali]       [Selanjutnya →]  │
└─────────────────────────────────────┘
         │ Zod validasi semua field
         ▼
LANGKAH 3: Gaya Hidup
┌─────────────────────────────────────┐
│  ● ● ● ○  Step 3 of 4              │
│                                     │
│  Status Merokok:     [▼ Pilih...]   │
│  Konsumsi Alkohol:   [▼ Pilih...]   │
│  Aktivitas Fisik:    [▼ Pilih...]   │
│                                     │
│  [← Kembali]       [Selanjutnya →]  │
└─────────────────────────────────────┘
         │ Zod validasi semua field
         ▼
LANGKAH 4: Konfirmasi & Submit
┌─────────────────────────────────────┐
│  ● ● ● ●  Step 4 of 4              │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  RINGKASAN DATA PASIEN     │    │
│  │                             │    │
│  │  Nama: Ahmad Sudrajat       │    │
│  │  Usia: 48 tahun             │    │
│  │  BMI: 28.5                  │    │
│  │  TD: 135/88 mmHg            │    │
│  │  ... (semua 11 atribut)     │    │
│  └─────────────────────────────┘    │
│                                     │
│  ⚠️ Pastikan data sudah benar      │
│                                     │
│  [← Kembali]     [🔍 Proses Skrining] │
└─────────────────────────────────────┘
         │ POST /api/screenings
         │ (loading spinner + skeleton)
         ▼
HASIL PREDIKSI
┌─────────────────────────────────────┐
│  ✅ Skrining Berhasil!              │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  🔴 RISIKO TINGGI           │    │
│  │  Confidence: 87%            │    │
│  │                             │    │
│  │  ████████████████ 87%       │    │
│  └─────────────────────────────┘    │
│                                     │
│  📊 Feature Importance:            │
│  [══ ECharts Horizontal Bar ══]     │
│                                     │
│  [📄 Unduh PDF]  [🔄 Skrining Baru] │
└─────────────────────────────────────┘
```

### 6.4 Zod Validation Schema

```typescript
// src/validations/screeningSchema.ts
import { z } from 'zod'

export const step1Schema = z.object({
  name: z.string().min(3, 'Nama minimal 3 karakter').max(100),
  nik: z.string().length(16, 'NIK harus 16 digit').regex(/^\d+$/, 'NIK harus berupa angka'),
  date_of_birth: z.string().refine(val => !isNaN(Date.parse(val)), 'Format tanggal tidak valid'),
  gender: z.enum(['male', 'female'], { message: 'Pilih jenis kelamin' }),
})

export const step2Schema = z.object({
  systolic_bp: z.number().int().min(70, 'Min 70 mmHg').max(250, 'Max 250 mmHg'),
  diastolic_bp: z.number().int().min(40, 'Min 40 mmHg').max(150, 'Max 150 mmHg'),
  bmi: z.number().min(10, 'Min 10').max(60, 'Max 60'),
  family_history: z.boolean(),
  diabetes: z.boolean(),
  cholesterol_level: z.enum(['normal', 'borderline', 'high'], { message: 'Pilih kadar kolesterol' }),
})

export const step3Schema = z.object({
  smoking_status: z.enum(['never', 'former', 'current'], { message: 'Pilih status merokok' }),
  alcohol_consumption: z.enum(['none', 'moderate', 'heavy'], { message: 'Pilih konsumsi alkohol' }),
  physical_activity: z.enum(['low', 'moderate', 'high'], { message: 'Pilih aktivitas fisik' }),
})

// Combined schema for API submission
export const screeningSchema = step1Schema.merge(step2Schema).merge(step3Schema).extend({
  age: z.number().int().min(18).max(100),
})
```

### 6.5 Dark/Light Theme System

```
┌────────────────────────────────────────────────────────┐
│                    THEME SYSTEM                        │
│                                                        │
│  themeStore.ts                                         │
│  ├── isDark: boolean (persisted to localStorage)       │
│  ├── toggleTheme(): void                               │
│  └── initTheme(): void (check system preference)       │
│                                                        │
│  globals.css                                           │
│  ├── :root { --background: 0 0% 100%; ... }           │
│  ├── .dark { --background: 222.2 84% 4.9%; ... }     │
│  └── Semua warna via CSS variables                     │
│                                                        │
│  ThemeToggle.vue                                       │
│  ├── Sun/Moon icon toggle                              │
│  ├── Smooth rotation animation                         │
│  └── System preference detection                       │
│                                                        │
│  Tailwind Config                                       │
│  └── darkMode: 'class' (toggle via .dark class)       │
│                                                        │
└────────────────────────────────────────────────────────┘

Light Mode                    Dark Mode
┌──────────────────┐          ┌──────────────────┐
│  bg: white       │          │  bg: slate-950    │
│  text: slate-900 │    🌓    │  text: slate-50   │
│  card: white     │  ─────→  │  card: slate-900  │
│  border: gray-200│          │  border: slate-800│
│  primary: teal   │          │  primary: teal    │
│  accent: blue    │          │  accent: blue     │
└──────────────────┘          └──────────────────┘
```

---

## Fase 7: Integrasi End-to-End

### 7.1 Checklist Integrasi

```
[ ] Frontend → Nginx → Backend (HTTPS API call)
[ ] Backend → ML Engine (internal HTTP call)
[ ] Backend → PostgreSQL (database query)
[ ] Frontend → Sanctum CSRF flow
[ ] Login → Session cookie → Authenticated API call
[ ] Screening form → Prediction → Dashboard update
[ ] RBAC enforcement per role
[ ] Error handling chain (ML → Backend → Frontend → Toast)
```

### 7.2 Testing Integrasi Manual

```bash
# 1. Test CSRF Cookie
curl -v -k https://localhost/sanctum/csrf-cookie
# Expected: Set-Cookie: XSRF-TOKEN=...

# 2. Test Login
curl -k -X POST https://localhost/api/login \
  -H "Content-Type: application/json" \
  -H "X-XSRF-TOKEN: <token_dari_step_1>" \
  -b "cookies.txt" -c "cookies.txt" \
  -d '{"email":"dokter@hypertension.id","password":"password"}'
# Expected: 200 OK + session cookie

# 3. Test Screening
curl -k -X POST https://localhost/api/screenings \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -b "cookies.txt" \
  -d '{
    "patient": {"name":"Test Patient","nik":"3201234567890001","date_of_birth":"1975-03-15","gender":"male"},
    "screening_data": {"age":48,"gender":"male","bmi":28.5,"smoking_status":"former","alcohol_consumption":"moderate","physical_activity":"low","family_history":true,"diabetes":false,"systolic_bp":135,"diastolic_bp":88,"cholesterol_level":"high"}
  }'
# Expected: 201 Created + prediction result

# 4. Test ML Engine Health (dari backend container)
docker compose exec backend curl http://ml-engine:8000/health
# Expected: {"status":"healthy","model_loaded":true}
```

### 7.3 Error Handling Flow

```
ML Engine Error (500)
    │
    ▼
Backend catches → MLEngineException
    │
    ├── Retry 3x (exponential backoff: 500ms, 1s, 2s)
    │
    ├── Still fails → Log error (without patient data!)
    │
    ├── Return 503 → {"error": "ML service temporarily unavailable"}
    │
    ▼
Frontend receives 503
    │
    ├── TanStack Query automatic retry (3x)
    │
    ├── Still fails → Toast notification (error)
    │
    └── User sees: "⚠️ Layanan prediksi sedang tidak tersedia. Silakan coba lagi."
```

---

## Fase 8: Testing & Quality Assurance

### 8.1 Test Matrix

| Layer | Tool | Command | Coverage Target |
|-------|------|---------|----------------|
| Backend Unit | PHPUnit | `docker compose exec backend php artisan test --testsuite=Unit` | 80%+ |
| Backend Feature | PHPUnit | `docker compose exec backend php artisan test --testsuite=Feature` | 70%+ |
| ML Engine Unit | pytest | `docker compose exec ml-engine pytest tests/ -v` | 90%+ |
| Frontend Unit | Vitest | `docker compose exec frontend npm run test:unit` | 70%+ |
| E2E | Cypress/Playwright | `npx cypress run` | Critical paths |

### 8.2 Key Tests

```
Backend Tests:
├── AuthTest.php
│   ├── test_user_can_login_with_valid_credentials
│   ├── test_user_cannot_login_with_invalid_credentials
│   ├── test_unauthenticated_user_cannot_access_api
│   └── test_user_can_logout
├── RBACTest.php
│   ├── test_perawat_cannot_access_admin_routes
│   ├── test_dokter_can_access_dashboard
│   └── test_admin_can_manage_users
├── ScreeningTest.php
│   ├── test_can_create_screening_with_valid_data
│   ├── test_cannot_create_screening_with_invalid_data
│   ├── test_screening_triggers_ml_prediction
│   └── test_screening_stores_prediction_result
└── MLEngineServiceTest.php
    ├── test_service_handles_timeout_gracefully
    ├── test_service_retries_on_failure
    └── test_service_sanitizes_log_output

ML Engine Tests:
├── test_preprocessing.py
│   ├── test_label_encoding_maps_correctly
│   ├── test_minmax_scaling_produces_0_to_1
│   ├── test_static_values_match_training_set
│   └── test_unknown_category_raises_error
├── test_prediction.py
│   ├── test_model_loads_successfully
│   ├── test_prediction_returns_valid_risk_level
│   ├── test_probabilities_sum_to_one
│   ├── test_feature_importance_has_11_features
│   └── test_inference_time_under_500ms
└── test_api.py
    ├── test_health_endpoint_returns_200
    ├── test_predict_endpoint_validates_input
    └── test_predict_endpoint_returns_valid_response
```

---

## Fase 9: Deployment Production

### 9.1 Pre-Production Checklist

```
Security:
[x] APP_DEBUG=false
[x] Ganti semua default passwords
[x] Gunakan SSL certificate yang valid (Let's Encrypt)
[x] Disable docs endpoint di FastAPI
[x] Set CORS origins secara spesifik
[x] Enable rate limiting

Performance:
[x] Laravel config:cache
[x] Laravel route:cache
[x] Laravel view:cache
[x] Frontend npm run build (production)
[x] Nginx gzip compression
[x] PostgreSQL connection pooling

Monitoring:
[x] Health check endpoints aktif
[x] Log rotation dikonfigurasi
[x] Disk space monitoring
[x] Backup strategy untuk PostgreSQL
```

### 9.2 Production Docker Compose Override

```yaml
# docker-compose.prod.yml
version: "3.9"

services:
  nginx:
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt:ro    # Real SSL certs
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"

  frontend:
    build:
      target: production              # Use production stage

  backend:
    build:
      target: production
    environment:
      - APP_ENV=production
      - APP_DEBUG=false
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "10"

  ml-engine:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
    logging:
      driver: json-file
      options:
        max-size: "20m"
        max-file: "5"

  postgres:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
    logging:
      driver: json-file
      options:
        max-size: "20m"
        max-file: "5"
```

### 9.3 Backup Strategy

```bash
# Backup PostgreSQL (daily cron)
docker compose exec postgres pg_dump -U hyper_admin hypertension_db > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20240115.sql | docker compose exec -T postgres psql -U hyper_admin hypertension_db
```

---

## Fase 10: Monitoring & Maintenance

### 10.1 Health Check Dashboard

```bash
#!/bin/bash
# health-check.sh — Jalankan setiap 5 menit via cron

echo "=== System Health Check ==="
echo "Time: $(date)"
echo ""

# Check Nginx
echo -n "Nginx: "
curl -sf -o /dev/null -w "%{http_code}" https://localhost/ && echo " ✅ OK" || echo " ❌ DOWN"

# Check Backend
echo -n "Backend: "
curl -sf -o /dev/null -w "%{http_code}" https://localhost/api/health && echo " ✅ OK" || echo " ❌ DOWN"

# Check ML Engine (via backend)
echo -n "ML Engine: "
docker compose exec -T backend curl -sf http://ml-engine:8000/health | grep -q "healthy" && echo " ✅ OK" || echo " ❌ DOWN"

# Check PostgreSQL
echo -n "PostgreSQL: "
docker compose exec -T postgres pg_isready -U hyper_admin > /dev/null 2>&1 && echo " ✅ OK" || echo " ❌ DOWN"

# Disk usage
echo ""
echo "Disk Usage:"
docker system df
```

### 10.2 Maintenance Tasks

| Task | Frekuensi | Command |
|------|-----------|---------|
| Database backup | Harian | `pg_dump` |
| Log rotation | Mingguan | Docker log driver |
| Docker image prune | Bulanan | `docker image prune -f` |
| SSL cert renewal | 60 hari | `certbot renew` |
| Dependency update | Bulanan | `composer update`, `npm update`, `pip update` |
| Security audit | Bulanan | `npm audit`, `composer audit` |

### 10.3 Scaling Considerations

```
Horizontal Scaling (Future):
├── Nginx: Load balance ke multiple backend instances
├── Backend: Stateless — scale dengan replicas
├── ML Engine: Scale berdasarkan inference load
├── PostgreSQL: Read replicas untuk query dashboard
└── Redis: Session storage + cache (future addition)

Vertical Scaling:
├── ML Engine: Alokasi lebih banyak CPU/RAM
├── PostgreSQL: Tuning postgresql.conf
└── Nginx: Worker processes = CPU cores
```

---

## 📝 Ringkasan Walkthrough

| Fase | Status | Deskripsi |
|------|--------|-----------|
| 1. Pemahaman Arsitektur | 📘 Baca | Konsep microservices, topologi, alur data |
| 2. Setup Environment | ⚙️ Setup | Install Docker, clone, config .env |
| 3. Build Infrastructure | 🏗️ Build | Docker Compose, Dockerfiles, networking |
| 4. Backend Laravel | 🔧 Code | API Gateway, auth, RBAC, migrations |
| 5. ML Engine | 🤖 Code | FastAPI, preprocessing, XGBoost |
| 6. Frontend Vue.js | 🎨 Code | SPA, form skrining, dashboard |
| 7. Integrasi | 🔗 Test | End-to-end testing, error handling |
| 8. QA Testing | ✅ Test | Unit tests, feature tests, E2E |
| 9. Production Deploy | 🚀 Deploy | SSL, optimization, security hardening |
| 10. Monitoring | 📊 Maintain | Health checks, backups, scaling |

---

<p align="center">
  <strong>Happy Building! 🏥✨</strong><br>
  Sistem Deteksi Dini Risiko Hipertensi
</p>
