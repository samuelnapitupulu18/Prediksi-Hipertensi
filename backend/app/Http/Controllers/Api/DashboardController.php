<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\DashboardService;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    protected $dashboardService;

    public function __construct(DashboardService $dashboardService)
    {
        $this->dashboardService = $dashboardService;
    }

    public function stats()
    {
        return response()->json([
            'data' => $this->dashboardService->getStats()
        ]);
    }

    public function riskDistribution()
    {
        return response()->json([
            'data' => $this->dashboardService->getRiskDistribution()
        ]);
    }

    public function featureImportance()
    {
        return response()->json([
            'data' => $this->dashboardService->getAggregateFeatureImportance()
        ]);
    }
    
    public function monthlyTrend()
    {
        return response()->json([
            'data' => $this->dashboardService->getMonthlyTrend()
        ]);
    }
}
