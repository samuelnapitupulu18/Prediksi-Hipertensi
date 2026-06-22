<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Patient extends Model
{
    use HasFactory;

    protected $fillable = [
        'nik',
        'name',
        'date_of_birth',
        'gender',
        'phone_number',
        'address'
    ];

    public function screenings()
    {
        return $this->hasMany(Screening::class);
    }
}
