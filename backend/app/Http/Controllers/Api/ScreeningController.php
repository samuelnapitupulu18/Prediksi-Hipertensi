<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Patient;
use App\Models\Screening;
use App\Models\Prediction;
use App\Services\MLEngineService;
use App\Services\ActivityLogService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class ScreeningController extends Controller
{
    protected MLEngineService $mlService;
    protected ActivityLogService $activityLogService;

    public function __construct(MLEngineService $mlService, ActivityLogService $activityLogService)
    {
        $this->mlService = $mlService;
        $this->activityLogService = $activityLogService;
    }

    public function index(Request $request)
    {
        $perPage = $request->query('per_page', 15);
        
        $query = Screening::with(['patient', 'prediction'])->latest();
        
        // If user is not super_admin, they might only see their own screenings
        if ($request->user()->role === 'perawat') {
            $query->where('user_id', $request->user()->id);
        }

        return response()->json($query->paginate($perPage));
    }

    public function store(Request $request)
    {
        // For brevity in this boilerplate, we use inline validation.
        // In a full implementation, use a FormRequest.
        $validated = $request->validate([
            // Patient Data
            'nik' => 'required|string|size:16',
            'name' => 'required|string|max:255',
            'date_of_birth' => 'required|date',
            'gender' => 'required|in:male,female',
            
            // Clinical Features
            'age' => 'required|integer|min:18|max:100',
            'bmi' => 'required|numeric|min:10|max:60',
            'smoking_status' => 'required|in:never,former,current',
            'alcohol_consumption' => 'required|in:none,moderate,heavy',
            'physical_activity' => 'required|in:low,moderate,high',
            'family_history' => 'required|boolean',
            'diabetes' => 'required|boolean',
            'systolic_bp' => 'required|integer|min:70|max:250',
            'diastolic_bp' => 'required|integer|min:40|max:150',
            'cholesterol_level' => 'required|in:normal,borderline,high',
        ]);

        try {
            DB::beginTransaction();

            // 1. Find or create patient
            $patient = Patient::firstOrCreate(
                ['nik' => $validated['nik']],
                [
                    'name' => $validated['name'],
                    'date_of_birth' => $validated['date_of_birth'],
                    'gender' => $validated['gender'],
                ]
            );

            // 2. Save screening data
            $screening = new Screening($validated);
            $screening->patient_id = $patient->id;
            $screening->user_id = $request->user()->id;
            $screening->save();

            // 3. Prepare payload for ML Engine
            $mlPayload = [
                'age' => $validated['age'],
                'gender' => $validated['gender'],
                'bmi' => $validated['bmi'],
                'smoking_status' => $validated['smoking_status'],
                'alcohol_consumption' => $validated['alcohol_consumption'],
                'physical_activity' => $validated['physical_activity'],
                'family_history' => $validated['family_history'],
                'diabetes' => $validated['diabetes'],
                'systolic_bp' => $validated['systolic_bp'],
                'diastolic_bp' => $validated['diastolic_bp'],
                'cholesterol_level' => $validated['cholesterol_level'],
            ];

            // 4. Call ML Engine via MLEngineService
            $predictionResult = $this->mlService->predict($mlPayload);

            // 5. Save Prediction Result
            $prediction = new Prediction([
                'screening_id' => $screening->id,
                'risk_level' => $predictionResult['risk_level'],
                'confidence_score' => $predictionResult['confidence_score'],
                'probability_distribution' => $predictionResult['probability'],
                'feature_importance' => $predictionResult['feature_importance'],
                'model_version' => $predictionResult['model_version'],
                'inference_time_ms' => $predictionResult['inference_time_ms'],
            ]);
            $prediction->save();

            // 6. Log activity (sanitized, no PHI)
            $this->activityLogService->log(
                'screening.created',
                "Skrining selesai dengan hasil risiko: {$predictionResult['risk_level']}",
                'App\Models\Screening',
                $screening->id
            );

            DB::commit();

            return response()->json([
                'message' => 'Skrining berhasil diproses.',
                'data' => [
                    'screening_id' => $screening->id,
                    'prediction' => $prediction
                ]
            ], 201);

        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Screening Error: ' . $e->getMessage());
            
            return response()->json([
                'message' => 'Gagal memproses skrining. ' . $e->getMessage()
            ], 500);
        }
    }
}
