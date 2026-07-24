// Harus sama dengan kolom `role` pada tabel users (lihat migration
// 2024_01_01_000001_create_users_table.php) dan RoleMiddleware di backend.
export type UserRole = 'super_admin' | 'dokter' | 'perawat'

export interface User {
  id: number
  name: string
  email: string
  role: UserRole
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}
