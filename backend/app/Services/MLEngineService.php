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
