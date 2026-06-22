import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'
import type { User, LoginCredentials } from '../types/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isInitializing = ref(true)

  const isAuthenticated = computed(() => !!user.value)
  const isSuperAdmin = computed(() => user.value?.role === 'super_admin')
  const isDokter = computed(() => user.value?.role === 'dokter')
  const isPerawat = computed(() => user.value?.role === 'perawat')

  async function fetchUser() {
    try {
      const response = await api.get('/user')
      user.value = response.data
    } catch (error) {
      user.value = null
    } finally {
      isInitializing.value = false
    }
  }

  async function login(credentials: LoginCredentials) {
    // 1. Fetch CSRF Cookie first
    await api.get('/sanctum/csrf-cookie', { baseURL: '' })
    
    // 2. Perform login
    const response = await api.post('/login', credentials)
    user.value = response.data.user
    return response.data
  }

  async function logout() {
    await api.post('/logout')
    user.value = null
  }

  return {
    user,
    isInitializing,
    isAuthenticated,
    isSuperAdmin,
    isDokter,
    isPerawat,
    login,
    logout,
    fetchUser
  }
})
