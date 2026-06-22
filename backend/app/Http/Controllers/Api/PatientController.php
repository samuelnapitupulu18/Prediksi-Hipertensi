<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\PatientService;
use App\Services\ActivityLogService;
use Illuminate\Http\Request;

class PatientController extends Controller
{
    protected $patientService;
    protected $activityLogService;

    public function __construct(PatientService $patientService, ActivityLogService $activityLogService)
    {
        $this->patientService = $patientService;
        $this->activityLogService = $activityLogService;
    }

    public function index(Request $request)
    {
        $search = $request->query('search');
        $patients = $this->patientService->getPatients($search);
        
        return response()->json($patients);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'nik' => 'required|string|size:16|unique:patients,nik',
            'name' => 'required|string|max:255',
            'date_of_birth' => 'required|date',
            'gender' => 'required|in:male,female',
            'phone' => 'nullable|string|max:15',
            'address' => 'nullable|string'
        ]);

        $patient = $this->patientService->createPatient($validated);
        
        $this->activityLogService->log(
            'patient.created',
            "Pasien baru didaftarkan: {$patient->name}",
            'App\Models\Patient',
            $patient->id
        );

        return response()->json([
            'message' => 'Pasien berhasil ditambahkan',
            'data' => $patient
        ], 201);
    }

    public function show($id)
    {
        $patient = $this->patientService->getPatientById($id);
        return response()->json(['data' => $patient]);
    }

    public function update(Request $request, $id)
    {
        $validated = $request->validate([
            'nik' => 'sometimes|required|string|size:16|unique:patients,nik,'.$id,
            'name' => 'sometimes|required|string|max:255',
            'date_of_birth' => 'sometimes|required|date',
            'gender' => 'sometimes|required|in:male,female',
            'phone' => 'nullable|string|max:15',
            'address' => 'nullable|string'
        ]);

        $patient = $this->patientService->updatePatient($id, $validated);

        $this->activityLogService->log(
            'patient.updated',
            "Data pasien diperbarui: {$patient->name}",
            'App\Models\Patient',
            $patient->id
        );

        return response()->json([
            'message' => 'Pasien berhasil diperbarui',
            'data' => $patient
        ]);
    }

    public function destroy($id)
    {
        $this->patientService->deletePatient($id);

        $this->activityLogService->log(
            'patient.deleted',
            "Data pasien dihapus (ID: {$id})",
            'App\Models\Patient',
            $id
        );

        return response()->json(['message' => 'Pasien berhasil dihapus']);
    }
}
