<template>
  <div class="relative flex min-h-screen bg-white dark:bg-slate-950 overflow-hidden transition-colors duration-500">
    <!-- Split Left: Animated Mesh Gradient & Quote -->
    <div class="hidden w-1/2 flex-col justify-between p-12 text-white lg:flex relative overflow-hidden">
      <!-- Animated Mesh Gradient Background -->
      <div class="absolute inset-0 bg-slate-900 z-0"></div>
      <div class="absolute -top-[25%] -left-[25%] w-[150%] h-[150%] bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-600/40 via-blue-900/40 to-slate-900/80 animate-[spin_60s_linear_infinite] z-0 blur-3xl"></div>
      <div class="absolute -bottom-[25%] -right-[25%] w-[150%] h-[150%] bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-indigo-500/30 via-slate-900/10 to-transparent animate-[spin_40s_linear_infinite_reverse] z-0 blur-3xl"></div>

      <div class="z-10 relative">
        <h1 class="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-100 to-white">
          HealthTech Enterprise
        </h1>
        <div class="mt-4 h-1 w-12 bg-blue-500 rounded-full"></div>
      </div>
      
      <div class="z-10 relative space-y-8">
        <!-- Abstract Decoration -->
        <div class="relative w-full max-w-sm aspect-square opacity-80 mix-blend-screen mb-12">
          <div class="absolute inset-0 rounded-full border border-blue-400/20 animate-[ping_3s_ease-in-out_infinite]"></div>
          <div class="absolute inset-4 rounded-full border border-blue-400/40 animate-[ping_4s_ease-in-out_infinite_reverse]"></div>
          <div class="absolute inset-8 rounded-full border border-blue-300/60 animate-pulse"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-blue-300/80"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.48 12H2"/></svg>
          </div>
        </div>

        <blockquote class="text-2xl font-medium leading-relaxed backdrop-blur-md bg-white/5 p-8 rounded-3xl border border-white/10 shadow-2xl relative overflow-hidden">
          <div class="absolute top-0 left-0 w-2 h-full bg-gradient-to-b from-blue-400 to-indigo-600"></div>
          "Pendeteksian dini adalah pertahanan terbaik melawan komplikasi kardiovaskular. Sistem cerdas ini mengintegrasikan presisi klinis dengan analisa Machine Learning untuk melindungi nyawa."
        </blockquote>
        <div class="flex items-center gap-5 mt-6 pl-4">
          <div class="h-14 w-14 rounded-full bg-gradient-to-br from-blue-400 to-indigo-600 p-[2px] shadow-lg shadow-blue-500/30">
            <div class="h-full w-full rounded-full bg-slate-900 flex items-center justify-center">
              <span class="font-bold text-lg">AF</span>
            </div>
          </div>
          <div>
            <p class="font-semibold text-lg">Dr. Alexander Fleming</p>
            <p class="text-xs text-blue-300 font-bold tracking-wider uppercase mt-1">Kardiolog & Penasihat Medis</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Split Right: Login Form -->
    <div class="flex w-full items-center justify-center lg:w-1/2 relative bg-slate-50 dark:bg-slate-950 transition-colors duration-500">
      
      <!-- Subtle Decorative Blobs for Glassmorphism effect -->
      <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div class="absolute -top-[10%] -left-[10%] h-[40%] w-[40%] rounded-full bg-blue-400/20 dark:bg-blue-600/10 blur-[100px]"></div>
        <div class="absolute bottom-[10%] -right-[10%] h-[50%] w-[50%] rounded-full bg-indigo-400/20 dark:bg-indigo-600/10 blur-[120px]"></div>
      </div>

      <Transition 
        appear
        enter-active-class="transition duration-1000 ease-out"
        enter-from-class="opacity-0 translate-y-12 scale-95"
        enter-to-class="opacity-100 translate-y-0 scale-100"
      >
        <div class="z-10 w-full max-w-md space-y-8 rounded-[2.5rem] bg-white/70 dark:bg-slate-900/70 p-10 shadow-[0_8px_40px_rgb(0,0,0,0.08)] ring-1 ring-slate-200 dark:ring-slate-800 backdrop-blur-2xl transition-all relative overflow-hidden">
          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500"></div>
          
          <div class="text-center">
            <div class="mx-auto h-16 w-16 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-2xl flex items-center justify-center mb-6 shadow-inner ring-1 ring-blue-100 dark:ring-blue-800/50">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
              Akses Platform
            </h2>
            <p class="mt-3 text-sm text-slate-500 dark:text-slate-400 font-medium">
              Silakan otentikasi identitas medis Anda
            </p>
          </div>
          
          <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
            <div class="space-y-5">
              <div class="space-y-1.5">
                <label for="email" class="block text-sm font-semibold text-slate-700 dark:text-slate-300">Email Klinis</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-slate-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                  </div>
                  <input 
                    v-model="email" 
                    id="email" 
                    type="email" 
                    required 
                    class="block w-full rounded-xl border-0 py-3.5 pl-12 pr-4 text-slate-900 dark:text-white bg-white dark:bg-slate-950/80 shadow-sm ring-1 ring-inset ring-slate-300 dark:ring-slate-700 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 dark:focus:ring-blue-500 sm:text-sm sm:leading-6 transition-all hover:bg-slate-50 dark:hover:bg-slate-900" 
                    placeholder="dr.nama@rs.local" 
                  />
                </div>
              </div>
              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <label for="password" class="block text-sm font-semibold text-slate-700 dark:text-slate-300">Kata Sandi</label>
                </div>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-slate-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                  </div>
                  <input 
                    v-model="password" 
                    id="password" 
                    type="password" 
                    required 
                    class="block w-full rounded-xl border-0 py-3.5 pl-12 pr-4 text-slate-900 dark:text-white bg-white dark:bg-slate-950/80 shadow-sm ring-1 ring-inset ring-slate-300 dark:ring-slate-700 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 dark:focus:ring-blue-500 sm:text-sm sm:leading-6 transition-all hover:bg-slate-50 dark:hover:bg-slate-900" 
                    placeholder="••••••••" 
                  />
                </div>
              </div>
            </div>

            <Transition
              enter-active-class="transition duration-300 ease-out"
              enter-from-class="transform -translate-y-2 opacity-0"
              enter-to-class="transform translate-y-0 opacity-100"
              leave-active-class="transition duration-200 ease-in"
              leave-from-class="transform translate-y-0 opacity-100"
              leave-to-class="transform -translate-y-2 opacity-0"
            >
              <div v-if="errorMsg" class="rounded-xl bg-red-50 dark:bg-red-900/30 p-4 text-sm text-red-600 dark:text-red-400 border border-red-200 dark:border-red-800/50 flex items-start gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0 mt-0.5"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
                <span>{{ errorMsg }}</span>
              </div>
            </Transition>

            <div class="pt-2">
              <button 
                type="submit" 
                :disabled="isLoading"
                class="group relative flex w-full justify-center items-center gap-2 rounded-xl bg-blue-600 px-4 py-3.5 text-sm font-bold text-white shadow-lg shadow-blue-500/30 hover:bg-blue-500 hover:shadow-blue-500/50 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2 dark:focus:ring-offset-slate-900 disabled:opacity-70 disabled:cursor-not-allowed transition-all duration-200 active:scale-[0.98] overflow-hidden"
              >
                <div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
                <svg v-if="isLoading" class="h-5 w-5 animate-spin text-white relative z-10" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                <span class="relative z-10 tracking-wide">{{ isLoading ? 'Membangun Sesi Aman...' : 'Masuk ke Sistem' }}</span>
                <svg v-if="!isLoading" class="h-4 w-4 transition-transform group-hover:translate-x-1 relative z-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
              </button>
            </div>
          </form>
        </div>
      </Transition>

      <!-- Footer Watermark for Login Page -->
      <div class="absolute bottom-6 text-center text-xs text-slate-400 dark:text-slate-500 w-full px-4 font-medium tracking-wide">
        Sistem Deteksi Dini Hipertensi - Dikembangkan oleh Samuel Alfred Richardo Napitupulu <br class="hidden sm:block"/> (D4 Teknologi Rekayasa Perangkat Lunak, Politeknik Negeri Medan)
      </div>
    </div>
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
      errorMsg.value = 'Kredensial tidak diakui oleh sistem.'
    } else {
      errorMsg.value = 'Terjadi galat jaringan. Periksa konektivitas.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
