<template>
  <div class="relative flex min-h-screen items-center justify-center bg-slate-50 dark:bg-slate-950 transition-colors duration-500 overflow-hidden">
    
    <!-- Subtle Background Decoration -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute -top-[20%] -left-[10%] h-[50%] w-[50%] rounded-full bg-blue-400/10 dark:bg-blue-600/5 blur-[120px]"></div>
      <div class="absolute -bottom-[20%] -right-[10%] h-[60%] w-[60%] rounded-full bg-indigo-400/10 dark:bg-indigo-600/5 blur-[140px]"></div>
    </div>

    <!-- Login Card -->
    <Transition 
      appear
      enter-active-class="transition duration-700 ease-out"
      enter-from-class="opacity-0 translate-y-8 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
    >
      <div class="z-10 w-full max-w-sm mx-4 sm:mx-auto">
        <!-- Logo & Title -->
        <div class="text-center mb-8">
          <div class="mx-auto h-16 w-16 bg-blue-600 rounded-2xl flex items-center justify-center mb-5 shadow-lg shadow-blue-500/30">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.48 12H2"/></svg>
          </div>
          <h1 class="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">Sistem Deteksi Dini</h1>
          <h2 class="text-2xl font-extrabold tracking-tight text-blue-600 dark:text-blue-400">Risiko Hipertensi</h2>
          <p class="mt-2 text-sm text-slate-500 dark:text-slate-400 font-medium">Masuk dengan akun tenaga kesehatan Anda</p>
        </div>

        <!-- Form Card -->
        <div class="rounded-2xl bg-white dark:bg-slate-900 p-8 shadow-xl shadow-slate-200/40 dark:shadow-slate-900/40 ring-1 ring-slate-200/60 dark:ring-slate-800/60">
          <form class="space-y-5" @submit.prevent="handleLogin">
            <!-- Email -->
            <div class="space-y-1.5">
              <label for="email" class="block text-sm font-semibold text-slate-700 dark:text-slate-300">Email</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-slate-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                </div>
                <input 
                  v-model="email" 
                  id="email" 
                  type="email" 
                  required 
                  class="block w-full rounded-xl border-0 py-3 pl-11 pr-4 text-slate-900 dark:text-white bg-slate-50 dark:bg-slate-800 ring-1 ring-inset ring-slate-200 dark:ring-slate-700 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 dark:focus:ring-blue-500 text-sm transition-all" 
                  placeholder="nama@email.com" 
                />
              </div>
            </div>

            <!-- Password -->
            <div class="space-y-1.5">
              <label for="password" class="block text-sm font-semibold text-slate-700 dark:text-slate-300">Kata Sandi</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-slate-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                </div>
                <input 
                  v-model="password" 
                  id="password" 
                  type="password" 
                  required 
                  class="block w-full rounded-xl border-0 py-3 pl-11 pr-4 text-slate-900 dark:text-white bg-slate-50 dark:bg-slate-800 ring-1 ring-inset ring-slate-200 dark:ring-slate-700 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 dark:focus:ring-blue-500 text-sm transition-all" 
                  placeholder="••••••••" 
                />
              </div>
            </div>

            <!-- Error Message -->
            <Transition
              enter-active-class="transition duration-300 ease-out"
              enter-from-class="transform -translate-y-2 opacity-0"
              enter-to-class="transform translate-y-0 opacity-100"
              leave-active-class="transition duration-200 ease-in"
              leave-from-class="transform translate-y-0 opacity-100"
              leave-to-class="transform -translate-y-2 opacity-0"
            >
              <div v-if="errorMsg" class="rounded-xl bg-red-50 dark:bg-red-900/30 p-3 text-sm text-red-600 dark:text-red-400 border border-red-200 dark:border-red-800/50 flex items-start gap-2.5">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0 mt-0.5"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
                <span>{{ errorMsg }}</span>
              </div>
            </Transition>

            <!-- Submit Button -->
            <button 
              type="submit" 
              :disabled="isLoading"
              class="flex w-full justify-center items-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-blue-500/25 hover:bg-blue-500 hover:shadow-blue-500/40 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2 dark:focus:ring-offset-slate-900 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200 active:scale-[0.98]"
            >
              <svg v-if="isLoading" class="h-5 w-5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              {{ isLoading ? 'Memproses...' : 'Masuk' }}
            </button>
          </form>
        </div>

        <!-- Footer -->
        <p class="mt-6 text-center text-[11px] text-slate-400 dark:text-slate-500 font-medium">
          Sistem Deteksi Dini Hipertensi — Dikembangkan oleh Samuel Alfred Richardo Napitupulu<br/>
          D4 Teknologi Rekayasa Perangkat Lunak, Politeknik Negeri Medan
        </p>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  isLoading.value = true
  errorMsg.value = ''
  
  try {
    await authStore.login({
      email: email.value,
      password: password.value
    })
    router.push({ name: 'dashboard' })
  } catch (error: any) {
    if (error.response?.status === 401) {
      errorMsg.value = 'Email atau kata sandi salah.'
    } else {
      errorMsg.value = 'Terjadi kesalahan jaringan. Silakan coba lagi.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
