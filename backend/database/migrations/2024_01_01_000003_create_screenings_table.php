<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('screenings', function (Blueprint $table) {
            $table->id();
            $table->foreignId('patient_id')->constrained()->onDelete('cascade');
            $table->foreignId('user_id')->constrained('users')->comment('Perawat/Dokter yang menginput');
            
            // 11 Clinical Features
            $table->integer('age');
            $table->enum('gender', ['male', 'female']);
            $table->float('bmi');
            $table->enum('smoking_status', ['never', 'former', 'current']);
            $table->enum('alcohol_consumption', ['none', 'moderate', 'heavy']);
            $table->enum('physical_activity', ['low', 'moderate', 'high']);
            $table->boolean('family_history');
            $table->boolean('diabetes');
            $table->integer('systolic_bp');
            $table->integer('diastolic_bp');
            $table->enum('cholesterol_level', ['normal', 'borderline', 'high']);
            
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('screenings');
    }
};
