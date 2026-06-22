<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('predictions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('screening_id')->constrained()->onDelete('cascade');
            
            $table->enum('risk_level', ['low', 'medium', 'high']);
            $table->float('confidence_score');
            
            // Storing probabilities as JSON
            $table->jsonb('probability_distribution');
            
            // Storing feature importance as JSON
            $table->jsonb('feature_importance');
            
            $table->string('model_version');
            $table->float('inference_time_ms');
            
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('predictions');
    }
};
