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
        'physical_activity',
        'family_history',
        'red_meat_consumption',
        'salt_consumption',
        'systolic_bp',
        'diastolic_bp',
    ];

    protected $casts = [
        'family_history' => 'boolean',
        'smoking_status' => 'boolean',
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
