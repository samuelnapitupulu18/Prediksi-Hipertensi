<?php

namespace App\Services;

use App\Models\Patient;
use Illuminate\Pagination\LengthAwarePaginator;

class PatientService
{
    /**
     * Ambil daftar pasien dengan pencarian dan paginasi.
     */
    public function getPatients(?string $search, int $perPage = 15): LengthAwarePaginator
    {
        $query = Patient::query()->latest();

        if ($search) {
            $query->where('name', 'ilike', '%' . $search . '%')
                  ->orWhere('nik', 'ilike', '%' . $search . '%');
        }

        return $query->paginate($perPage);
    }

    /**
     * Buat data pasien baru.
     */
    public function createPatient(array $data): Patient
    {
        return Patient::create($data);
    }

    /**
     * Dapatkan detail pasien.
     */
    public function getPatientById(int $id): Patient
    {
        return Patient::with(['screenings' => function($q) {
            $q->latest()->with('prediction');
        }])->findOrFail($id);
    }

    /**
     * Update data pasien.
     */
    public function updatePatient(int $id, array $data): Patient
    {
        $patient = Patient::findOrFail($id);
        $patient->update($data);
        return $patient;
    }

    /**
     * Hapus pasien.
     */
    public function deletePatient(int $id): bool
    {
        $patient = Patient::findOrFail($id);
        return $patient->delete();
    }
}
