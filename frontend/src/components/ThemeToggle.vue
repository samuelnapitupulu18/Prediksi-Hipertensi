<template>
  <button 
    @click="toggleDark()" 
    class="relative inline-flex items-center justify-center p-2 text-slate-500 transition-colors rounded-md hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
    aria-label="Toggle Dark Mode"
  >
    <!-- Sun icon for light mode (visible when dark) -->
    <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-yellow-400">
      <circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>
    </svg>
    <!-- Moon icon for dark mode (visible when light) -->
    <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-700">
      <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
    </svg>
  </button>
</template>

<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core'

// Menggunakan useDark dari VueUse, salah satu library Vue paling standar dan handal untuk DOM utils
// Ini otomatis menambahkan/menghapus class "dark" ke tag <html>
const isDark = useDark({
  selector: 'html',
  attribute: 'class',
  valueDark: 'dark',
  valueLight: '',
})

const toggleDark = useToggle(isDark)
</script>
