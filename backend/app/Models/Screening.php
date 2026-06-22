<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Screening extends Model
{
    use HasFactory;

    protected $fillable = [
        'patient_id',
        'user_id',
        'age',
        'gender',
        'bmi',
        'smoking_status',
        'alcohol_consumption',
        'physical_activity',
        'family_history',
        'diabetes',
        'systolic_bp',
        'diastolic_bp',
        'cholesterol_level'
    ];

    protected $casts = [
        'family_history' => 'boolean',
        'diabetes' => 'boolean',
    ];

    public function patient()
    {
        return $this->belongsTo(Patient::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function prediction()
    {
        return $this->hasOne(Prediction::class);
    }
}
