<?php

namespace App\Services;

use App\Models\ActivityLog;
use Illuminate\Support\Facades\Request;

class ActivityLogService
{
    /**
     * Catat aktivitas pengguna ke database.
     */
    public function log(string $action, string $description, ?string $entityType = null, ?int $entityId = null, ?int $userId = null)
    {
        return ActivityLog::create([
            'user_id' => $userId ?? auth()->id(),
            'action' => $action,
            'entity_type' => $entityType,
            'entity_id' => $entityId,
            'description' => $description,
            'ip_address' => Request::ip(),
            'user_agent' => Request::userAgent(),
        ]);
    }

    /**
     * Ambil daftar audit log dengan paginasi.
     */
    public function getLogs(int $perPage = 15)
    {
        return ActivityLog::with('user:id,name,role,email')
            ->orderBy('created_at', 'desc')
            ->paginate($perPage);
    }
}
