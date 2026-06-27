<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class RBACTest extends TestCase
{
    use RefreshDatabase;

    public function test_perawat_cannot_access_admin_routes()
    {
        $perawat = User::factory()->create(['role' => 'perawat']);

        $response = $this->actingAs($perawat)->getJson('/api/admin/users');

        $response->assertStatus(403);
    }

    public function test_dokter_can_access_dashboard()
    {
        $dokter = User::factory()->create(['role' => 'dokter']);

        // Since DashboardController->stats exists
        $response = $this->actingAs($dokter)->getJson('/api/dashboard/stats');

        $response->assertStatus(200);
    }

    public function test_admin_can_manage_users()
    {
        $admin = User::factory()->create(['role' => 'super_admin']);

        $response = $this->actingAs($admin)->getJson('/api/admin/users');

        $response->assertStatus(200);
    }
}
