<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\UserService;
use App\Services\ActivityLogService;
use Illuminate\Http\Request;

class UserController extends Controller
{
    protected $userService;
    protected $activityLogService;

    public function __construct(UserService $userService, ActivityLogService $activityLogService)
    {
        $this->userService = $userService;
        $this->activityLogService = $activityLogService;
    }

    public function index(Request $request)
    {
        $search = $request->query('search');
        $users = $this->userService->getUsers($search);
        
        return response()->json($users);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
            'role' => 'required|in:super_admin,dokter,perawat',
            'is_active' => 'boolean'
        ]);

        $user = $this->userService->createUser($validated);
        
        $this->activityLogService->log(
            'user.created',
            "Akun pengguna baru dibuat: {$user->email} ({$user->role})",
            'App\Models\User',
            $user->id
        );

        return response()->json([
            'message' => 'Pengguna berhasil ditambahkan',
            'data' => $user
        ], 201);
    }

    public function show($id)
    {
        $user = $this->userService->getUserById($id);
        return response()->json(['data' => $user]);
    }

    public function update(Request $request, $id)
    {
        $validated = $request->validate([
            'name' => 'sometimes|required|string|max:255',
            'email' => 'sometimes|required|string|email|max:255|unique:users,email,'.$id,
            'password' => 'nullable|string|min:8|confirmed',
            'role' => 'sometimes|required|in:super_admin,dokter,perawat',
            'is_active' => 'boolean'
        ]);

        $user = $this->userService->updateUser($id, $validated);

        $this->activityLogService->log(
            'user.updated',
            "Akun pengguna diperbarui: {$user->email}",
            'App\Models\User',
            $user->id
        );

        return response()->json([
            'message' => 'Pengguna berhasil diperbarui',
            'data' => $user
        ]);
    }

    public function destroy($id)
    {
        // Cegah admin menghapus dirinya sendiri
        if (auth()->id() == $id) {
            return response()->json(['message' => 'Anda tidak dapat menghapus akun Anda sendiri'], 400);
        }

        $user = $this->userService->getUserById($id);
        $email = $user->email;
        $this->userService->deleteUser($id);

        $this->activityLogService->log(
            'user.deleted',
            "Akun pengguna dihapus: {$email}",
            'App\Models\User',
            $id
        );

        return response()->json(['message' => 'Pengguna berhasil dihapus']);
    }
}
