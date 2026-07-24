<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        // CATATAN: statefulApi() sengaja TIDAK diaktifkan.
        //
        // Frontend memakai autentikasi stateless dengan bearer token Sanctum
        // (lihat frontend/src/services/api.ts — withCredentials: false).
        // Bila statefulApi() aktif, setiap permintaan dari browser yang berasal
        // dari SANCTUM_STATEFUL_DOMAINS akan diperlakukan sebagai permintaan
        // berbasis session sehingga menuntut token CSRF, dan login gagal dengan
        // HTTP 419 "CSRF token mismatch".
        $middleware->alias([
            'role' => \App\Http\Middleware\RoleMiddleware::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        //
    })->create();
