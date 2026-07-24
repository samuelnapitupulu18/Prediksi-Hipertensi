<template>
  <div class="flex h-screen overflow-hidden bg-slate-50 dark:bg-slate-950 transition-colors duration-300">
    
    <!-- Mobile Backdrop -->
    <div 
      v-if="isMobileMenuOpen" 
      @click="isMobileMenuOpen = false" 
      class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-20 lg:hidden"
    ></div>

    <!-- Sidebar -->
    <aside 
      class="w-64 flex-shrink-0 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col transition-transform duration-300 z-30 fixed lg:static inset-y-0 left-0"
      :class="isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
    >
      <div class="h-16 flex items-center px-6 border-b border-slate-100 dark:border-slate-800">
        <div class="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3 shadow-lg shadow-blue-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.48 12H2"/></svg>
        </div>
        <h2 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">HT-Detect</h2>
      </div>
      
      <nav class="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <!-- Dasbor -->
        <router-link 
          to="/dashboard" 
          @click="isMobileMenuOpen = false"
          class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
          :class="[$route.name === 'dashboard' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
        >
          <div v-if="$route.name === 'dashboard'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
          Dasbor Utama
        </router-link>
        
        <!-- Skrining Baru -->
        <router-link 
          to="/screening/new" 
          @click="isMobileMenuOpen = false"
          class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
          :class="[$route.name === 'screening-new' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
        >
          <div v-if="$route.name === 'screening-new'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M15 2H9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1Z"/><path d="M12 11v6"/><path d="M9 14h6"/></svg>
          Skrining Baru
        </router-link>

        <!-- Riwayat Skrining -->
        <router-link 
          to="/screening/history" 
          @click="isMobileMenuOpen = false"
          class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
          :class="[$route.name === 'screening-history' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
        >
          <div v-if="$route.name === 'screening-history'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/></svg>
          Riwayat Skrining
        </router-link>

        <!-- Daftar Pasien -->
        <router-link 
          to="/patients" 
          @click="isMobileMenuOpen = false"
          class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
          :class="[$route.name === 'patient-list' || $route.name === 'patient-detail' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
        >
          <div v-if="$route.name === 'patient-list' || $route.name === 'patient-detail'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Daftar Pasien
        </router-link>

        <!-- Analisis XAI -->
        <router-link 
          to="/xai" 
          @click="isMobileMenuOpen = false"
          class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
          :class="[$route.name === 'xai-dashboard' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
        >
          <div v-if="$route.name === 'xai-dashboard'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
          Analisis XAI
        </router-link>

        <!-- Perbandingan Model -->
        <router-link 
          to="/model-accuracy" 
          @click="isMobileMenuOpen = false"
          class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
          :class="[$route.name === 'model-accuracy' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
        >
          <div v-if="$route.name === 'model-accuracy'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M16 20V4H8v16"/><path d="M12 14V4"/><path d="M4 20V10"/><path d="M20 20v-6"/></svg>
          Perbandingan Model
        </router-link>

        <!-- Uji Prediksi Live -->
        <router-link 
          to="/live-comparison" 
          @click="isMobileMenuOpen = false"
          class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
          :class="[$route.name === 'live-comparison' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
        >
          <div v-if="$route.name === 'live-comparison'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><polygon points="6 3 20 12 6 21 6 3"/></svg>
          Uji Prediksi Live
        </router-link>

        <!-- ══════════ Khusus Super Admin ══════════ -->
        <template v-if="authStore.isSuperAdmin">
          <div class="pt-4 mt-2 border-t border-slate-100 dark:border-slate-800">
            <p class="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              Administrasi
            </p>
          </div>

          <router-link
            to="/admin/users"
            @click="isMobileMenuOpen = false"
            class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
            :class="[$route.name === 'admin-users' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
          >
            <div v-if="$route.name === 'admin-users'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            Manajemen Pengguna
          </router-link>

          <router-link
            to="/admin/audit-logs"
            @click="isMobileMenuOpen = false"
            class="relative flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-semibold transition-all duration-200 group overflow-hidden"
            :class="[$route.name === 'admin-audit-logs' ? 'text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200']"
          >
            <div v-if="$route.name === 'admin-audit-logs'" class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)] rounded-r-full"></div>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/></svg>
            Jejak Audit
          </router-link>
        </template>
      </nav>

      <!-- Sidebar Footer -->
      <div class="p-4 border-t border-slate-100 dark:border-slate-800">
        <div class="mb-4 flex items-center justify-between px-2">
          <div class="flex items-center gap-3">
            <div class="h-9 w-9 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center border border-slate-200 dark:border-slate-700">
              <span class="text-sm font-bold text-slate-600 dark:text-slate-300">{{ authStore.user?.name?.charAt(0) || 'U' }}</span>
            </div>
            <div>
              <p class="text-sm font-bold text-slate-800 dark:text-slate-200 truncate w-32">{{ authStore.user?.name }}</p>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400 capitalize">{{ getRoleLabel(authStore.user?.role) }}</p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button @click="handleLogout" class="flex-1 flex items-center justify-center gap-2 px-3 py-2.5 text-sm font-bold text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-500/10 hover:bg-red-100 dark:hover:bg-red-500/20 rounded-xl transition-colors active:scale-95">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>
            Keluar
          </button>
          <div class="bg-slate-50 dark:bg-slate-800 rounded-xl p-0.5 border border-slate-200 dark:border-slate-700">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden relative">
      <!-- Desktop Header -->
      <header class="absolute top-0 w-full h-16 flex items-center justify-between px-8 bg-white dark:bg-slate-900 border-b border-slate-200/50 dark:border-slate-800/50 z-30 transition-colors hidden lg:flex shadow-sm">
        <div class="flex items-center gap-2 text-sm font-medium text-slate-500 dark:text-slate-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          <span class="mx-1">/</span>
          <span class="capitalize text-slate-900 dark:text-white font-semibold">{{ $route.name?.toString().replace(/-/g, ' ') || 'Dashboard' }}</span>
        </div>
        <div class="flex items-center gap-4">
          <div class="text-xs font-semibold px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full flex items-center gap-1.5 border border-green-200 dark:border-green-800">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Sistem Online
          </div>
        </div>
      </header>

      <!-- Mobile Header -->
      <header class="lg:hidden h-16 flex items-center justify-between px-4 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 z-10">
        <div class="flex items-center gap-3">
          <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="p-2 -ml-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
          </button>
          <div class="flex items-center gap-2">
            <div class="h-6 w-6 bg-blue-600 rounded flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.48 12H2"/></svg>
            </div>
            <h2 class="text-lg font-bold text-slate-900 dark:text-white">HT-Detect</h2>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <div class="flex-1 overflow-y-auto p-6 md:p-8 lg:pt-24 relative">
        <router-view v-slot="{ Component }">
          <transition name="page-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>

      <!-- Footer -->
      <footer class="py-4 text-center border-t border-slate-200/50 dark:border-slate-800/50 bg-white/40 dark:bg-slate-900/40 backdrop-blur-sm text-[10px] sm:text-xs text-slate-500 dark:text-slate-500 font-medium">
        Sistem Deteksi Dini Hipertensi — Dikembangkan oleh Samuel Alfred Richardo Napitupulu <br class="hidden sm:block"/> (D4 Teknologi Rekayasa Perangkat Lunak, Politeknik Negeri Medan)
      </footer>
    </main>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import ThemeToggle from '../components/ThemeToggle.vue'

const router = useRouter()
const authStore = useAuthStore()
const isMobileMenuOpen = ref(false)

function getRoleLabel(role?: string): string {
  if (role === 'dokter') return 'Dokter'
  if (role === 'perawat') return 'Perawat'
  return role || ''
}

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.page-slide-enter-active,
.page-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-slide-enter-from {
  opacity: 0;
  transform: translateY(10px) scale(0.99);
}

.page-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.99);
}
</style>
