<?php

namespace App\Services;

use Exception;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class MLEngineService
{
    protected string $baseUrl;
    protected int $timeout;
    protected int $retryTimes;
    protected int $retrySleep;

    public function __construct()
    {
        $this->baseUrl = env('ML_ENGINE_BASE_URL', 'http://ml-engine:8000');
        $this->timeout = (int) env('ML_ENGINE_TIMEOUT', 30);
        $this->retryTimes = (int) env('ML_ENGINE_RETRY_TIMES', 3);
        $this->retrySleep = (int) env('ML_ENGINE_RETRY_SLEEP', 500);
    }

    /**
     * Sends clinical features to the ML Engine to get a risk prediction.
     */
    public function predict(array $clinicalFeatures): array
    {
        try {
            $response = Http::timeout($this->timeout)
                ->retry($this->retryTimes, $this->retrySleep)
                ->post("{$this->baseUrl}/predict", $clinicalFeatures);

            if ($response->successful()) {
                return $response->json();
            }

            if ($response->status() === 422) {
                Log::error('ML Engine Validation Error', ['response' => $response->json()]);
                throw new Exception('Data tidak valid sesuai skema ML Engine.');
            }

            if ($response->status() === 503) {
                throw new Exception('Model prediksi belum siap digunakan. Silakan coba lagi nanti.');
            }

            Log::error('ML Engine Error', [
                'status' => $response->status(),
                'body' => $response->body()
            ]);
            
            throw new Exception('Gagal menghubungi mesin prediksi. Terjadi kesalahan pada server ML.');

        } catch (\Illuminate\Http\Client\ConnectionException $e) {
            Log::error('ML Engine Connection Timeout/Error', ['message' => $e->getMessage()]);
            throw new Exception('Gagal menghubungi layanan kecerdasan buatan (timeout).');
        } catch (Exception $e) {
            throw $e;
        }
    }

    /**
     * Menjalankan perbandingan XGBoost Default vs XGBoost + SGO pada ML Engine.
     *
     * Proses ini melatih puluhan model sungguhan, sehingga memakai timeout
     * tersendiri yang jauh lebih longgar daripada permintaan prediksi biasa.
     */
    public function compareOptimization(array $config): array
    {
        $timeout = (int) env('ML_ENGINE_OPTIMIZE_TIMEOUT', 1800);

        try {
            $response = Http::timeout($timeout)
                ->post("{$this->baseUrl}/optimize/compare", $config);

            if ($response->successful()) {
                return $response->json();
            }

            Log::error('ML Engine Optimization Error', [
                'status' => $response->status(),
                'body' => $response->body(),
            ]);

            throw new Exception(
                $response->json('detail') ?? 'Gagal menjalankan perbandingan optimasi pada ML Engine.'
            );
        } catch (\Illuminate\Http\Client\ConnectionException $e) {
            Log::error('ML Engine Optimization Timeout', ['message' => $e->getMessage()]);
            throw new Exception(
                'Proses optimasi melebihi batas waktu. Kurangi jumlah iterasi atau ukuran populasi.'
            );
        }
    }

    /**
     * Uji waktu eksekusi kedua model pada jumlah iterasi boosting tertentu.
     *
     * Jauh lebih ringan daripada compareOptimization() karena hanya melatih dua
     * model, sehingga memakai timeout yang lebih pendek.
     */
    public function compareTiming(array $config): array
    {
        $timeout = (int) env('ML_ENGINE_TIMING_TIMEOUT', 300);

        try {
            $response = Http::timeout($timeout)
                ->post("{$this->baseUrl}/optimize/timing", $config);

            if ($response->successful()) {
                return $response->json();
            }

            Log::error('ML Engine Timing Error', [
                'status' => $response->status(),
                'body' => $response->body(),
            ]);

            throw new Exception(
                $response->json('detail') ?? 'Gagal menjalankan uji waktu pada ML Engine.'
            );
        } catch (\Illuminate\Http\Client\ConnectionException $e) {
            Log::error('ML Engine Timing Timeout', ['message' => $e->getMessage()]);
            throw new Exception('Uji waktu melebihi batas. Kurangi jumlah iterasi atau pengulangan.');
        }
    }

    /**
     * Metadata model produksi yang sedang dimuat ML Engine.
     *
     * Berisi metrik hasil pengukuran nyata saat pelatihan, sehingga antarmuka
     * tidak perlu menyimpan satu pun angka performa di sisi frontend.
     */
    public function modelInfo(): array
    {
        try {
            $response = Http::timeout(15)->get("{$this->baseUrl}/model-info");

            if ($response->successful()) {
                return $response->json();
            }

            throw new Exception('Metadata model belum tersedia pada ML Engine.');
        } catch (\Illuminate\Http\Client\ConnectionException $e) {
            Log::error('ML Engine model-info unreachable', ['message' => $e->getMessage()]);
            throw new Exception('Gagal menghubungi ML Engine untuk mengambil metadata model.');
        }
    }

    public function healthCheck(): bool
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/health");
            return $response->successful();
        } catch (\Exception $e) {
            return false;
        }
    }
}
