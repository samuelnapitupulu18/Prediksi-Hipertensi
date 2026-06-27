<?php

namespace Tests\Feature;

use App\Models\User;
use App\Models\Patient;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Services\MLEngineService;
use Mockery\MockInterface;

class ScreeningTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        
        // Mock the MLEngineService so we don't actually call FastAPI during tests
        $this->mock(MLEngineService::class, function (MockInterface $mock) {
            $mock->shouldReceive('predict')->andReturn([
                'risk_level' => 'high',
                'confidence_score' => 0.88,
                'probability' => ['low' => 0.02, 'medium' => 0.10, 'high' => 0.88],
                'feature_importance' => [['feature' => 'age', 'importance' => 0.5]],
                'model_version' => '1.0.0-mock',
                'inference_time_ms' => 15
            ]);
        });
    }

    public function test_can_create_screening_with_valid_data()
    {
        $dokter = User::factory()->create(['role' => 'dokter']);

        $payload = [
            'nik' => '1234567890123456',
            'name' => 'John Doe',
            'date_of_birth' => '1980-01-01',
            'gender' => 'male',
            'age' => 44,
            'bmi' => 25.5,
            'smoking_status' => 'never',
            'alcohol_consumption' => 'none',
            'physical_activity' => 'moderate',
            'family_history' => false,
            'diabetes' => false,
            'systolic_bp' => 120,
            'diastolic_bp' => 80,
            'cholesterol_level' => 'normal',
        ];

        $response = $this->actingAs($dokter)->postJson('/api/screenings', $payload);

        $response->assertStatus(201)
                 ->assertJsonStructure([
                     'message',
                     'data' => [
                         'screening_id',
                         'prediction'
                     ]
                 ]);
        
        $this->assertDatabaseHas('patients', [
            'nik' => '1234567890123456'
        ]);
        
        $this->assertDatabaseHas('predictions', [
            'risk_level' => 'high'
        ]);
    }

    public function test_cannot_create_screening_with_invalid_data()
    {
        $dokter = User::factory()->create(['role' => 'dokter']);

        $payload = [
            'nik' => 'short', // invalid
            'age' => 200, // max is 100
        ];

        $response = $this->actingAs($dokter)->postJson('/api/screenings', $payload);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['nik', 'age', 'name']);
    }
}
