<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Prediction extends Model
{
    use HasFactory;

    protected $fillable = [
        'screening_id',
        'risk_level',
        'confidence_score',
        'probability_distribution',
        'feature_importance',
        'model_version',
        'inference_time_ms'
    ];

    protected $casts = [
        'probability_distribution' => 'array',
        'feature_importance' => 'array',
    ];

    public function screening()
    {
        return $this->belongsTo(Screening::class);
    }
}
