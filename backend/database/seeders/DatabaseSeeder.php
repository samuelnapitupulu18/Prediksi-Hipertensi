<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Patient;
use App\Models\Screening;
use App\Models\Prediction;
use App\Models\ActivityLog;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Bobot kepentingan fitur global dari model XGBoost-SGO.
     * Nilai ini identik dengan yang dikembalikan ML Engine
     * (ml-engine/app/models/xgboost_model.py::get_feature_importances).
     */
    private array $featureImportance = [
        ['feature' => 'systolic_bp',          'importance' => 0.4352, 'label' => 'Tekanan Darah Sistolik (TDS)'],
        ['feature' => 'diastolic_bp',         'importance' => 0.2145, 'label' => 'Tekanan Darah Diastolik (TDD)'],
        ['feature' => 'bmi',                  'importance' => 0.1420, 'label' => 'Indeks Massa Tubuh (IMT)'],
        ['feature' => 'age',                  'importance' => 0.0912, 'label' => 'Usia'],
        ['feature' => 'salt_consumption',     'importance' => 0.0415, 'label' => 'Konsumsi Garam'],
        ['feature' => 'family_history',       'importance' => 0.0310, 'label' => 'Riwayat Keluarga'],
        ['feature' => 'smoking_status',       'importance' => 0.0212, 'label' => 'Status Perokok'],
        ['feature' => 'red_meat_consumption', 'importance' => 0.0125, 'label' => 'Konsumsi Daging Merah'],
        ['feature' => 'physical_activity',    'importance' => 0.0074, 'label' => 'Aktivitas Fisik'],
        ['feature' => 'gender',               'importance' => 0.0035, 'label' => 'Jenis Kelamin'],
    ];

    public function run(): void
    {
        $users = $this->seedUsers();
        $this->seedScreeningHistory($users);
    }

    /**
     * Akun tenaga kesehatan. Password semua akun: "password".
     */
    private function seedUsers(): array
    {
        $admin = User::firstOrCreate(
            ['email' => 'admin@admin.com'],
            ['name' => 'Super Admin', 'password' => Hash::make('password'), 'role' => 'super_admin']
        );

        $dokter = User::firstOrCreate(
            ['email' => 'dokter@admin.com'],
            ['name' => 'Dr. Budi', 'password' => Hash::make('password'), 'role' => 'dokter']
        );

        $perawat = User::firstOrCreate(
            ['email' => 'perawat@admin.com'],
            ['name' => 'Suster Siti', 'password' => Hash::make('password'), 'role' => 'perawat']
        );

        return ['admin' => $admin, 'dokter' => $dokter, 'perawat' => $perawat];
    }

    /**
     * Riwayat skrining historis: pasien + data klinis + hasil prediksi.
     *
     * Nilai risk_level, confidence_score, dan probability_distribution di bawah
     * BUKAN karangan — semuanya diambil dari keluaran ML Engine (XGBoost-SGO)
     * untuk kombinasi fitur klinis yang bersangkutan, lalu dibekukan di sini agar
     * proses seeding tidak bergantung pada ML Engine yang sedang berjalan.
     *
     * Digit ke-7 s/d 12 pada NIK = tanggal lahir DDMMYY (perempuan: DD + 40),
     * mengikuti format Dukcapil.
     *
     * months_ago menyebar data ke 6 bulan terakhir supaya grafik tren bulanan
     * pada dashboard terisi.
     */
    private function seedScreeningHistory(array $users): void
    {
        $dokterId  = $users['dokter']->id;
        $perawatId = $users['perawat']->id;

        $records = [
            [
                'nik' => '3171011204750001', 'name' => 'Budi Harjo', 'dob' => '1975-04-12', 'sex' => 'male',
                'phone' => '081234567890', 'address' => 'Jl. Merdeka No. 1, Jakarta',
                'age' => 51, 'bmi' => 26.5, 'family_history' => true, 'physical_activity' => 'moderate',
                'smoking_status' => true, 'red_meat_consumption' => 'moderate', 'salt_consumption' => 'high',
                'systolic_bp' => 135, 'diastolic_bp' => 85,
                'risk' => 'medium', 'confidence' => 0.6110, 'prob' => ['low' => 0.2944, 'medium' => 0.6110, 'high' => 0.0946],
                'ms' => 12.5, 'months_ago' => 5, 'day' => 4, 'by' => $dokterId,
            ],
            [
                'nik' => '3171016311820002', 'name' => 'Siti Aminah', 'dob' => '1982-11-23', 'sex' => 'female',
                'phone' => '081298765432', 'address' => 'Jl. Sudirman No. 45, Bandung',
                'age' => 43, 'bmi' => 22.1, 'family_history' => false, 'physical_activity' => 'high',
                'smoking_status' => false, 'red_meat_consumption' => 'low', 'salt_consumption' => 'low',
                'systolic_bp' => 110, 'diastolic_bp' => 75,
                'risk' => 'medium', 'confidence' => 0.9110, 'prob' => ['low' => 0.0411, 'medium' => 0.9110, 'high' => 0.0479],
                'ms' => 10.2, 'months_ago' => 5, 'day' => 18, 'by' => $perawatId,
            ],
            [
                'nik' => '3171011502680003', 'name' => 'Agus Setiawan', 'dob' => '1968-02-15', 'sex' => 'male',
                'phone' => '081312341234', 'address' => 'Jl. Thamrin No. 9, Surabaya',
                'age' => 58, 'bmi' => 31.2, 'family_history' => true, 'physical_activity' => 'low',
                'smoking_status' => true, 'red_meat_consumption' => 'high', 'salt_consumption' => 'high',
                'systolic_bp' => 160, 'diastolic_bp' => 100,
                'risk' => 'high', 'confidence' => 0.5805, 'prob' => ['low' => 0.3302, 'medium' => 0.0893, 'high' => 0.5805],
                'ms' => 11.1, 'months_ago' => 4, 'day' => 7, 'by' => $dokterId,
            ],
            [
                'nik' => '3171014807900004', 'name' => 'Rina Marlina', 'dob' => '1990-07-08', 'sex' => 'female',
                'phone' => '085612345678', 'address' => 'Jl. Gatot Subroto No. 22, Medan',
                'age' => 36, 'bmi' => 24.8, 'family_history' => false, 'physical_activity' => 'moderate',
                'smoking_status' => false, 'red_meat_consumption' => 'moderate', 'salt_consumption' => 'moderate',
                'systolic_bp' => 120, 'diastolic_bp' => 80,
                'risk' => 'low', 'confidence' => 0.4618, 'prob' => ['low' => 0.4618, 'medium' => 0.3649, 'high' => 0.1733],
                'ms' => 9.8, 'months_ago' => 4, 'day' => 21, 'by' => $perawatId,
            ],
            [
                'nik' => '3171013010550005', 'name' => 'Hendra Gunawan', 'dob' => '1955-10-30', 'sex' => 'male',
                'phone' => '081198761234', 'address' => 'Jl. Diponegoro No. 88, Semarang',
                'age' => 70, 'bmi' => 28.4, 'family_history' => true, 'physical_activity' => 'low',
                'smoking_status' => false, 'red_meat_consumption' => 'high', 'salt_consumption' => 'high',
                'systolic_bp' => 145, 'diastolic_bp' => 90,
                'risk' => 'high', 'confidence' => 0.5329, 'prob' => ['low' => 0.3833, 'medium' => 0.0839, 'high' => 0.5329],
                'ms' => 13.0, 'months_ago' => 3, 'day' => 3, 'by' => $dokterId,
            ],
            [
                'nik' => '3171015703880006', 'name' => 'Dewi Lestari', 'dob' => '1988-03-17', 'sex' => 'female',
                'phone' => '081377889900', 'address' => 'Jl. Ahmad Yani No. 12, Yogyakarta',
                'age' => 38, 'bmi' => 23.5, 'family_history' => false, 'physical_activity' => 'high',
                'smoking_status' => false, 'red_meat_consumption' => 'low', 'salt_consumption' => 'moderate',
                'systolic_bp' => 115, 'diastolic_bp' => 76,
                'risk' => 'medium', 'confidence' => 0.9141, 'prob' => ['low' => 0.0395, 'medium' => 0.9141, 'high' => 0.0464],
                'ms' => 10.7, 'months_ago' => 3, 'day' => 16, 'by' => $perawatId,
            ],
            [
                'nik' => '3171010509720007', 'name' => 'Joko Prasetyo', 'dob' => '1972-09-05', 'sex' => 'male',
                'phone' => '082145678901', 'address' => 'Jl. Pemuda No. 5, Solo',
                'age' => 53, 'bmi' => 29.8, 'family_history' => true, 'physical_activity' => 'low',
                'smoking_status' => true, 'red_meat_consumption' => 'high', 'salt_consumption' => 'high',
                'systolic_bp' => 152, 'diastolic_bp' => 96,
                'risk' => 'high', 'confidence' => 0.5824, 'prob' => ['low' => 0.3287, 'medium' => 0.0889, 'high' => 0.5824],
                'ms' => 12.1, 'months_ago' => 2, 'day' => 6, 'by' => $dokterId,
            ],
            [
                'nik' => '3171014212950008', 'name' => 'Maya Sari', 'dob' => '1995-12-02', 'sex' => 'female',
                'phone' => '085799001122', 'address' => 'Jl. Veteran No. 30, Malang',
                'age' => 30, 'bmi' => 21.4, 'family_history' => false, 'physical_activity' => 'high',
                'smoking_status' => false, 'red_meat_consumption' => 'low', 'salt_consumption' => 'low',
                'systolic_bp' => 108, 'diastolic_bp' => 70,
                'risk' => 'medium', 'confidence' => 0.9110, 'prob' => ['low' => 0.0411, 'medium' => 0.9110, 'high' => 0.0479],
                'ms' => 9.4, 'months_ago' => 2, 'day' => 19, 'by' => $perawatId,
            ],
            [
                'nik' => '3171012106600009', 'name' => 'Bambang Wijaya', 'dob' => '1960-06-21', 'sex' => 'male',
                'phone' => '081233445566', 'address' => 'Jl. Imam Bonjol No. 17, Denpasar',
                'age' => 66, 'bmi' => 30.5, 'family_history' => true, 'physical_activity' => 'low',
                'smoking_status' => false, 'red_meat_consumption' => 'high', 'salt_consumption' => 'high',
                'systolic_bp' => 158, 'diastolic_bp' => 98,
                'risk' => 'high', 'confidence' => 0.5329, 'prob' => ['low' => 0.3833, 'medium' => 0.0839, 'high' => 0.5329],
                'ms' => 12.8, 'months_ago' => 1, 'day' => 5, 'by' => $dokterId,
            ],
            [
                'nik' => '3171015401780010', 'name' => 'Nurul Hidayah', 'dob' => '1978-01-14', 'sex' => 'female',
                'phone' => '085611223344', 'address' => 'Jl. Kartini No. 63, Palembang',
                'age' => 48, 'bmi' => 27.2, 'family_history' => true, 'physical_activity' => 'moderate',
                'smoking_status' => false, 'red_meat_consumption' => 'moderate', 'salt_consumption' => 'high',
                'systolic_bp' => 138, 'diastolic_bp' => 88,
                'risk' => 'medium', 'confidence' => 0.6229, 'prob' => ['low' => 0.2545, 'medium' => 0.6229, 'high' => 0.1226],
                'ms' => 11.6, 'months_ago' => 1, 'day' => 22, 'by' => $perawatId,
            ],
            [
                'nik' => '3171010908850011', 'name' => 'Ahmad Fauzi', 'dob' => '1985-08-09', 'sex' => 'male',
                'phone' => '081455667788', 'address' => 'Jl. Cendrawasih No. 8, Makassar',
                'age' => 40, 'bmi' => 25.1, 'family_history' => false, 'physical_activity' => 'moderate',
                'smoking_status' => true, 'red_meat_consumption' => 'moderate', 'salt_consumption' => 'moderate',
                'systolic_bp' => 128, 'diastolic_bp' => 82,
                'risk' => 'low', 'confidence' => 0.5039, 'prob' => ['low' => 0.5039, 'medium' => 0.3305, 'high' => 0.1656],
                'ms' => 10.9, 'months_ago' => 0, 'day' => 4, 'by' => $dokterId,
            ],
            [
                'nik' => '3171016705630012', 'name' => 'Ratna Dewi', 'dob' => '1963-05-27', 'sex' => 'female',
                'phone' => '082199887766', 'address' => 'Jl. Melati No. 41, Pekanbaru',
                'age' => 63, 'bmi' => 29.3, 'family_history' => true, 'physical_activity' => 'low',
                'smoking_status' => false, 'red_meat_consumption' => 'high', 'salt_consumption' => 'high',
                'systolic_bp' => 150, 'diastolic_bp' => 94,
                'risk' => 'high', 'confidence' => 0.5873, 'prob' => ['low' => 0.3243, 'medium' => 0.0884, 'high' => 0.5873],
                'ms' => 12.3, 'months_ago' => 0, 'day' => 9, 'by' => $perawatId,
            ],
        ];

        foreach ($records as $r) {
            $timestamp = now()
                ->subMonths($r['months_ago'])
                ->startOfMonth()
                ->addDays($r['day'])
                ->setTime(9, 30);

            $patient = Patient::firstOrCreate(
                ['nik' => $r['nik']],
                [
                    'name' => $r['name'],
                    'date_of_birth' => $r['dob'],
                    'gender' => $r['sex'],
                    'phone_number' => $r['phone'],
                    'address' => $r['address'],
                    'created_at' => $timestamp,
                    'updated_at' => $timestamp,
                ]
            );

            $screening = Screening::firstOrCreate(
                ['patient_id' => $patient->id, 'created_at' => $timestamp],
                [
                    'user_id' => $r['by'],
                    'age' => $r['age'],
                    'gender' => $r['sex'],
                    'bmi' => $r['bmi'],
                    'family_history' => $r['family_history'],
                    'physical_activity' => $r['physical_activity'],
                    'smoking_status' => $r['smoking_status'],
                    'red_meat_consumption' => $r['red_meat_consumption'],
                    'salt_consumption' => $r['salt_consumption'],
                    'systolic_bp' => $r['systolic_bp'],
                    'diastolic_bp' => $r['diastolic_bp'],
                    'updated_at' => $timestamp,
                ]
            );

            Prediction::firstOrCreate(
                ['screening_id' => $screening->id],
                [
                    // Kolom JSON di-cast 'array' pada model — jangan json_encode manual.
                    'risk_level' => $r['risk'],
                    'confidence_score' => $r['confidence'],
                    'probability_distribution' => $r['prob'],
                    'feature_importance' => $this->featureImportance,
                    'model_version' => '1.0.0-sgo-mock',
                    'inference_time_ms' => $r['ms'],
                    'created_at' => $timestamp,
                    'updated_at' => $timestamp,
                ]
            );

            ActivityLog::firstOrCreate(
                [
                    'action' => 'screening.created',
                    'entity_type' => 'App\Models\Screening',
                    'entity_id' => $screening->id,
                ],
                [
                    'user_id' => $r['by'],
                    'description' => "Skrining selesai dengan hasil risiko: {$r['risk']}",
                    'ip_address' => '127.0.0.1',
                    'user_agent' => 'Seeder/1.0',
                    'created_at' => $timestamp,
                    'updated_at' => $timestamp,
                ]
            );
        }
    }
}
