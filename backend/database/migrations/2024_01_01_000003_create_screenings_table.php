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
            
            // 10 Clinical Features based on dataset
            $table->integer('age');
            $table->enum('gender', ['male', 'female']);
            $table->float('bmi');
            $table->boolean('family_history');
            $table->enum('physical_activity', ['low', 'moderate', 'high']);
            $table->boolean('smoking_status');
            $table->enum('red_meat_consumption', ['low', 'moderate', 'high']);
            $table->enum('salt_consumption', ['low', 'moderate', 'high']);
            $table->integer('systolic_bp');
            $table->integer('diastolic_bp');
            
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('screenings');
    }
};
