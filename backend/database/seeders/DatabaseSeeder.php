<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // Seed Super Admin
        User::firstOrCreate([
            'email' => 'admin@admin.com',
        ], [
            'name' => 'Super Admin',
            'password' => Hash::make('password'),
            'role' => 'super_admin',
        ]);

        // Seed Dokter
        User::firstOrCreate([
            'email' => 'dokter@admin.com',
        ], [
            'name' => 'Dr. Budi',
            'password' => Hash::make('password'),
            'role' => 'dokter',
        ]);
        
        // Seed Perawat
        User::firstOrCreate([
            'email' => 'perawat@admin.com',
        ], [
            'name' => 'Suster Siti',
            'password' => Hash::make('password'),
            'role' => 'perawat',
        ]);
    }
}
