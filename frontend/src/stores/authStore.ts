import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'
import type { User, LoginCredentials } from '../types/auth'

// =====================================================================
// Auth Store — autentikasi memakai bearer token Laravel Sanctum.
// Token disimpan di localStorage sehingga sesi tetap aktif walau tab
// ditutup (fungsi ini menggantikan fitur "remember me" bawaan Laravel).
//
// Tidak ada mode demo/offline: bila backend tidak dapat dihubungi, login
// gagal dengan pesan yang jelas.
// =====================================================================

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isInitializing = ref(true)

  const isAuthenticated = computed(() => !!user.value)
  const isDokter = computed(() => user.value?.role === 'dokter')
  const isPerawat = computed(() => user.value?.role === 'perawat')
  const isSuperAdmin = computed(() => user.value?.role === 'super_admin')

  // Both roles have equal access — this helper checks if user is authenticated with a valid role
  const hasAccess = computed(() => isDokter.value || isPerawat.value)

  function clearSession() {
    user.value = null
    localStorage.removeItem('auth_token')
    delete api.defaults.headers.common['Authorization']
  }

  async function fetchUser() {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      user.value = null
      isInitializing.value = false
      return
    }

    try {
      const { data } = await api.get('/user')
      user.value = data
    } catch {
      clearSession()
    } finally {
      isInitializing.value = false
    }
  }

  // Vue Router menjalankan navigasi pertama saat router dipasang — yaitu
  // SEBELUM fetchUser() selesai. Tanpa penjagaan ini, memuat ulang halaman
  // (F5) atau membuka URL langsung akan dianggap belum login dan dilempar
  // ke halaman login meskipun tokennya masih sah.
  //
  // ensureInitialized() mengembalikan promise yang sama untuk semua pemanggil,
  // sehingga pengecekan token hanya berjalan satu kali.
  let initPromise: Promise<void> | null = null

  function ensureInitialized(): Promise<void> {
    if (!initPromise) initPromise = fetchUser()
    return initPromise
  }

  async function login(credentials: LoginCredentials) {
    const { data } = await api.post('/login', credentials)
    user.value = data.user
    localStorage.setItem('auth_token', data.token)
    api.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
    return data
  }

  async function logout() {
    try {
      await api.post('/logout')
    } catch {
      // Abaikan kegagalan logout di server — sesi lokal tetap dibersihkan
    }
    clearSession()
  }

  return {
    user,
    isInitializing,
    isAuthenticated,
    isDokter,
    isPerawat,
    isSuperAdmin,
    hasAccess,
    login,
    logout,
    fetchUser,
    ensureInitialized
  }
})
