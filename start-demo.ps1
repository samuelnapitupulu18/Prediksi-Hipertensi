# =============================================================================
# HT-Detect — Skrip Menjalankan Sistem untuk Demonstrasi / Presentasi
# =============================================================================
# Menjalankan ketiga komponen sistem di perangkat lokal:
#
#   1. ML Engine (FastAPI + XGBoost-SGO) .... http://127.0.0.1:8000
#   2. Backend   (Laravel API) .............. http://127.0.0.1:8001
#   3. Frontend  (Vue 3 + Vite) ............. http://localhost:5173
#
# Database MySQL diasumsikan SUDAH berjalan di 127.0.0.1:3307 (user: root).
#
# Cara pakai — klik kanan file ini > "Run with PowerShell", atau jalankan:
#   powershell -ExecutionPolicy Bypass -File start-demo.ps1
# =============================================================================

$ErrorActionPreference = 'Stop'

$root    = $PSScriptRoot
$php     = 'C:\laragon\bin\php\php-8.3.29-nts-Win32-vs16-x64\php.exe'
$mysql   = 'C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe'
$pyVenv  = Join-Path $root 'ml-engine\.venv\Scripts\python.exe'

function Write-Step($text) { Write-Host "`n>> $text" -ForegroundColor Cyan }
function Write-Ok($text)   { Write-Host "   OK  $text" -ForegroundColor Green }
function Write-Bad($text)  { Write-Host "   !!  $text" -ForegroundColor Red }

Write-Host '============================================' -ForegroundColor Yellow
Write-Host ' HT-Detect - Menyiapkan sistem untuk demo' -ForegroundColor Yellow
Write-Host '============================================' -ForegroundColor Yellow

# --- 1. Prasyarat ------------------------------------------------------------
Write-Step 'Memeriksa prasyarat'

if (-not (Test-Path $php))    { Write-Bad "PHP 8.3 tidak ditemukan di $php"; exit 1 }
Write-Ok 'PHP 8.3'

if (-not (Test-Path $pyVenv)) { Write-Bad "Python venv ML Engine tidak ditemukan di $pyVenv"; exit 1 }
Write-Ok 'Python venv ML Engine'

$dbUp = Test-NetConnection -ComputerName 127.0.0.1 -Port 3307 -InformationLevel Quiet -WarningAction SilentlyContinue
if (-not $dbUp) { Write-Bad 'MySQL di port 3307 tidak aktif. Nyalakan dulu MySQL (Laragon > Start All).'; exit 1 }
Write-Ok 'MySQL 127.0.0.1:3307'

# --- 2. Database -------------------------------------------------------------
Write-Step 'Memeriksa database db_hipertensi'

$count = & $mysql -h 127.0.0.1 -P 3307 -u root -N -B -e "SELECT COUNT(*) FROM db_hipertensi.screenings;" 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($count)) {
    Write-Host '   Database belum ada / kosong - membangun ulang dari migrasi + seeder...' -ForegroundColor Yellow
    & $mysql -h 127.0.0.1 -P 3307 -u root -e "CREATE DATABASE IF NOT EXISTS db_hipertensi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    Push-Location (Join-Path $root 'backend')
    & $php artisan migrate --seed --force
    Pop-Location
    Write-Ok 'Database dibangun'
} else {
    Write-Ok "Database siap ($($count.Trim()) data skrining)"
}

# --- 3. Menjalankan layanan --------------------------------------------------
Write-Step 'Menjalankan ML Engine (port 8000)'
Start-Process powershell -ArgumentList @(
    '-NoExit', '-Command',
    "Set-Location '$root\ml-engine'; & '$pyVenv' -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
) -WindowStyle Normal
Write-Ok 'Jendela ML Engine terbuka'

Write-Step 'Menjalankan Backend Laravel (port 8001)'
Start-Process powershell -ArgumentList @(
    '-NoExit', '-Command',
    "Set-Location '$root\backend'; & '$php' artisan serve --host=127.0.0.1 --port=8001"
) -WindowStyle Normal
Write-Ok 'Jendela Backend terbuka'

Write-Step 'Menjalankan Frontend Vite (port 5173)'
Start-Process powershell -ArgumentList @(
    '-NoExit', '-Command',
    "Set-Location '$root\frontend'; npm run dev"
) -WindowStyle Normal
Write-Ok 'Jendela Frontend terbuka'

# --- 4. Menunggu layanan siap ------------------------------------------------
Write-Step 'Menunggu seluruh layanan siap'

function Wait-Url($url, $label, $maxTries = 40) {
    for ($i = 1; $i -le $maxTries; $i++) {
        try {
            Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3 | Out-Null
            Write-Ok "$label siap"
            return $true
        } catch {
            if ($_.Exception.Response) { Write-Ok "$label siap"; return $true }
            Start-Sleep -Milliseconds 1500
        }
    }
    Write-Bad "$label belum merespons - cek jendela terminalnya"
    return $false
}

$mlOk = Wait-Url 'http://127.0.0.1:8000/health' 'ML Engine'
$beOk = Wait-Url 'http://127.0.0.1:8001/api/user' 'Backend Laravel'
$feOk = Wait-Url 'http://localhost:5173/' 'Frontend'

# --- 5. Selesai --------------------------------------------------------------
Write-Host ''
Write-Host '============================================' -ForegroundColor Yellow
if ($mlOk -and $beOk -and $feOk) {
    Write-Host ' SISTEM SIAP DIGUNAKAN' -ForegroundColor Green
    Write-Host ''
    Write-Host '  Buka  : http://localhost:5173' -ForegroundColor White
    Write-Host ''
    Write-Host '  Akun demo (password semua: password)' -ForegroundColor White
    Write-Host '    Dokter      : dokter@admin.com'
    Write-Host '    Perawat     : perawat@admin.com'
    Write-Host '    Super Admin : admin@admin.com'
    Start-Process 'http://localhost:5173'
} else {
    Write-Host ' SEBAGIAN LAYANAN BELUM SIAP' -ForegroundColor Red
    Write-Host ' Periksa jendela terminal yang terbuka untuk melihat pesan errornya.'
}
Write-Host '============================================' -ForegroundColor Yellow
Write-Host ''
Write-Host 'Untuk menghentikan: tutup ketiga jendela terminal yang terbuka.' -ForegroundColor DarkGray
