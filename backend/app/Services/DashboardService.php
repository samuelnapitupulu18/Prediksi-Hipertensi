<?php

namespace App\Services;

use App\Models\Screening;
use App\Models\Prediction;
use App\Models\Patient;
use Illuminate\Support\Facades\DB;

class DashboardService
{
    /**
     * Get overall statistics for the dashboard.
     */
    public function getStats()
    {
        $totalScreenings = Screening::count();
        $totalPatients = Patient::count();
        
        $highRiskCount = Prediction::where('risk_level', 'high')->count();
        $lowRiskCount = Prediction::where('risk_level', 'low')->count();

        // Calculate simple trend (comparing this month to previous month could be added)
        
        return [
            'total_screenings' => $totalScreenings,
            'total_patients' => $totalPatients,
            'high_risk_count' => $highRiskCount,
            'low_risk_count' => $lowRiskCount,
            'high_risk_percentage' => $totalScreenings > 0 ? round(($highRiskCount / $totalScreenings) * 100, 1) : 0,
            'low_risk_percentage' => $totalScreenings > 0 ? round(($lowRiskCount / $totalScreenings) * 100, 1) : 0,
        ];
    }

    /**
     * Get risk distribution.
     */
    public function getRiskDistribution()
    {
        $distribution = Prediction::select('risk_level', DB::raw('count(*) as total'))
            ->groupBy('risk_level')
            ->get()
            ->pluck('total', 'risk_level')
            ->toArray();

        return [
            'low' => $distribution['low'] ?? 0,
            'medium' => $distribution['medium'] ?? 0,
            'high' => $distribution['high'] ?? 0,
        ];
    }

    /**
     * Get aggregated feature importance.
     * We average the feature importance across all predictions to see which features contribute the most overall.
     */
    public function getAggregateFeatureImportance()
    {
        // This is a simplified approach. For large datasets, this should be pre-aggregated in a cron job or materialized view.
        $predictions = Prediction::whereNotNull('feature_importance')->get();
        
        $aggregate = [];
        $count = $predictions->count();

        if ($count === 0) {
            return [];
        }

        foreach ($predictions as $prediction) {
            $features = $prediction->feature_importance; // assuming it's cast to array in model
            if (is_array($features)) {
                foreach ($features as $feature) {
                    $name = $feature['feature'] ?? null;
                    if ($name) {
                        if (!isset($aggregate[$name])) {
                            $aggregate[$name] = [
                                'feature' => $name,
                                'label' => $feature['label'] ?? $name,
                                'importance' => 0
                            ];
                        }
                        $aggregate[$name]['importance'] += $feature['importance'];
                    }
                }
            }
        }

        // Calculate average
        foreach ($aggregate as &$item) {
            $item['importance'] = $item['importance'] / $count;
        }

        // Sort descending
        usort($aggregate, function($a, $b) {
            return $b['importance'] <=> $a['importance'];
        });

        return $aggregate;
    }

    /**
     * Get monthly trend of screenings.
     */
    public function getMonthlyTrend()
    {
        // Get last 6 months trend
        $trend = Screening::select(
            DB::raw('extract(month from created_at) as month'),
            DB::raw('count(*) as total')
        )
        ->where('created_at', '>=', now()->subMonths(6))
        ->groupBy('month')
        ->orderBy('month')
        ->get();

        return $trend;
    }
}
