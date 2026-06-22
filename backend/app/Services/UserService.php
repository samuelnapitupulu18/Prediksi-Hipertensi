<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Pagination\LengthAwarePaginator;

class UserService
{
    /**
     * Ambil daftar pengguna.
     */
    public function getUsers(?string $search, int $perPage = 15): LengthAwarePaginator
    {
        $query = User::query()->latest();

        if ($search) {
            $query->where('name', 'ilike', '%' . $search . '%')
                  ->orWhere('email', 'ilike', '%' . $search . '%');
        }

        return $query->paginate($perPage);
    }

    /**
     * Buat data pengguna baru.
     */
    public function createUser(array $data): User
    {
        $data['password'] = Hash::make($data['password']);
        return User::create($data);
    }

    /**
     * Dapatkan detail pengguna.
     */
    public function getUserById(int $id): User
    {
        return User::findOrFail($id);
    }

    /**
     * Update data pengguna.
     */
    public function updateUser(int $id, array $data): User
    {
        $user = User::findOrFail($id);
        
        if (isset($data['password'])) {
            $data['password'] = Hash::make($data['password']);
        } else {
            unset($data['password']);
        }

        $user->update($data);
        return $user;
    }

    /**
     * Hapus pengguna.
     */
    public function deleteUser(int $id): bool
    {
        $user = User::findOrFail($id);
        return $user->delete();
    }
}
