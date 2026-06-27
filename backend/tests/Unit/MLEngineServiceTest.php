<?php

namespace Tests\Unit;

use App\Services\MLEngineService;
use App\Exceptions\MLEngineException;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class MLEngineServiceTest extends TestCase
{
    public function test_service_handles_timeout_gracefully()
    {
        Http::fake([
            '*/predict' => Http::response(null, 408) // Fake a timeout/error
        ]);

        $service = new MLEngineService();

        $this->expectException(MLEngineException::class);
        $service->predict(['age' => 40]);
    }

    public function test_service_returns_prediction_data()
    {
        $mockData = [
            'risk_level' => 'low',
            'confidence_score' => 0.9,
            'probability' => ['low' => 0.9, 'medium' => 0.05, 'high' => 0.05],
            'feature_importance' => [],
            'model_version' => '1.0.0',
            'inference_time_ms' => 10
        ];

        Http::fake([
            '*/predict' => Http::response($mockData, 200)
        ]);

        $service = new MLEngineService();
        $result = $service->predict(['age' => 30]);

        $this->assertEquals('low', $result['risk_level']);
        $this->assertEquals(0.9, $result['confidence_score']);
    }
}
