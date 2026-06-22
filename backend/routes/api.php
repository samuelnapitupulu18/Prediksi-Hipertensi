<?php

use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Api\ScreeningController;
use App\Http\Controllers\Api\PatientController;
use App\Http\Controllers\Api\DashboardController;
use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\Api\ActivityLogController;
use Illuminate\Support\Facades\Route;

// Public route for authentication
Route::post('/login', [LoginController::class, 'login']);

// Protected routes
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [LoginController::class, 'logout']);
    Route::get('/user', [LoginController::class, 'user']);
    
    // Dashboard analytics
    Route::prefix('dashboard')->group(function () {
        Route::get('/stats', [DashboardController::class, 'stats']);
        Route::get('/risk-distribution', [DashboardController::class, 'riskDistribution']);
        Route::get('/feature-importance', [DashboardController::class, 'featureImportance']);
        Route::get('/monthly-trend', [DashboardController::class, 'monthlyTrend']);
    });

    // Patient routes
    Route::apiResource('patients', PatientController::class);
    
    // Screening endpoints
    Route::post('/screenings', [ScreeningController::class, 'store']);
    Route::get('/screenings/{id}', [ScreeningController::class, 'show']);
    Route::get('/screenings', [ScreeningController::class, 'index']); // I need to implement index if it's missing
    
    // Admin only routes
    Route::middleware('role:super_admin')->prefix('admin')->group(function () {
        Route::apiResource('users', UserController::class);
        Route::get('audit-logs', [ActivityLogController::class, 'index']);
    });
});
