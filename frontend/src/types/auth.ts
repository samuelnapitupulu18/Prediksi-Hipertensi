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
