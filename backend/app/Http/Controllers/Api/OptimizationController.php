<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\MLEngineService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

/**
 * Menjembatani antarmuka dengan eksperimen optimasi pada ML Engine.
 *
 * Jumlah iterasi dan ukuran populasi SGO dikirim dari halaman "Uji Prediksi
 * Live", sehingga penguji dapat menentukannya sendiri saat demonstrasi.
 */
class OptimizationController extends Controller
{
    public function __construct(protected MLEngineService $mlService)
    {
    }

    /**
     * Metadata model produksi — dipakai halaman Perbandingan Model agar seluruh
     * angka yang tampil berasal dari hasil pelatihan, bukan ditulis di frontend.
     */
    public function modelInfo()
    {
        try {
            return response()->json(['data' => $this->mlService->modelInfo()]);
        } catch (\Exception $e) {
            Log::error('Model info failed: ' . $e->getMessage());

            return response()->json(['message' => $e->getMessage()], 500);
        }
    }

    /**
     * Uji akurasi & waktu eksekusi kedua model pada jumlah iterasi boosting
     * yang ditentukan sendiri untuk masing-masing model.
     */
    public function timing(Request $request)
    {
        $validated = $request->validate([
            'default_iterations' => 'required|integer|min:1|max:2000',
            'optimized_iterations' => 'required|integer|min:1|max:2000',
            'seed' => 'nullable|integer|min:0|max:9999',
            'repeats' => 'nullable|integer|min:1|max:10',
            'include_blood_pressure' => 'nullable|boolean',
        ]);

        try {
            $result = $this->mlService->compareTiming([
                'default_iterations' => (int) $validated['default_iterations'],
                'optimized_iterations' => (int) $validated['optimized_iterations'],
                'seed' => (int) ($validated['seed'] ?? 42),
                'repeats' => (int) ($validated['repeats'] ?? 3),
                'include_blood_pressure' => (bool) ($validated['include_blood_pressure'] ?? false),
            ]);

            return response()->json(['data' => $result]);
        } catch (\Exception $e) {
            Log::error('Timing comparison failed: ' . $e->getMessage());

            return response()->json(['message' => $e->getMessage()], 500);
        }
    }

    public function compare(Request $request)
    {
        $validated = $request->validate([
            'iterations' => 'required|integer|min:1|max:500',
            'population_size' => 'required|integer|min:3|max:50',
            'seed' => 'nullable|integer|min:0|max:9999',
            'include_blood_pressure' => 'nullable|boolean',
            'verification_runs' => 'nullable|integer|min:1|max:10',
        ]);

        try {
            $result = $this->mlService->compareOptimization([
                'iterations' => (int) $validated['iterations'],
                'population_size' => (int) $validated['population_size'],
                'seed' => (int) ($validated['seed'] ?? 42),
                'include_blood_pressure' => (bool) ($validated['include_blood_pressure'] ?? false),
                'verification_runs' => (int) ($validated['verification_runs'] ?? 1),
            ]);

            return response()->json(['data' => $result]);
        } catch (\Exception $e) {
            Log::error('Optimization comparison failed: ' . $e->getMessage());

            return response()->json([
                'message' => $e->getMessage(),
            ], 500);
        }
    }
}
