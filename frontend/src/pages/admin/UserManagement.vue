<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Manajemen Pengguna</h1>
        <p class="text-sm text-slate-500 dark:text-slate-400">Kelola akun akses untuk Dokter dan Perawat (Khusus Super Admin).</p>
      </div>
      <button class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors shadow-sm flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
        Tambah Pengguna
      </button>
    </div>

    <!-- User Table -->
    <div class="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-sm overflow-hidden transition-colors">
      <div class="relative w-full overflow-auto">
        <table class="w-full caption-bottom text-sm">
          <thead class="[&_tr]:border-b border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50">
            <tr class="border-b transition-colors hover:bg-slate-100/50 dark:hover:bg-slate-800/50">
              <th class="h-12 px-4 text-left align-middle font-medium text-slate-500 dark:text-slate-400">Nama Lengkap</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-slate-500 dark:text-slate-400">Email</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-slate-500 dark:text-slate-400">Peran (Role)</th>
              <th class="h-12 px-4 text-right align-middle font-medium text-slate-500 dark:text-slate-400">Aksi</th>
            </tr>
          </thead>
          <tbody class="[&_tr:last-child]:border-0 text-slate-700 dark:text-slate-300">
            <tr v-for="user in users" :key="user.id" class="border-b border-slate-100 dark:border-slate-800 transition-colors hover:bg-slate-50 dark:hover:bg-slate-800">
              <td class="p-4 align-middle font-medium">{{ user.name }}</td>
              <td class="p-4 align-middle">{{ user.email }}</td>
              <td class="p-4 align-middle">
                <span 
                  class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"
                  :class="{
                    'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400': user.role === 'super_admin',
                    'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400': user.role === 'dokter',
                    'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400': user.role === 'perawat'
                  }"
                >
                  {{ formatRole(user.role) }}
                </span>
              </td>
              <td class="p-4 align-middle text-right">
                <div class="flex items-center justify-end gap-2">
                  <button class="p-2 text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors rounded-md hover:bg-slate-100 dark:hover:bg-slate-800" aria-label="Edit">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                  </button>
                  <button class="p-2 text-slate-400 hover:text-red-600 dark:hover:text-red-400 transition-colors rounded-md hover:bg-slate-100 dark:hover:bg-slate-800" aria-label="Hapus" :disabled="user.role === 'super_admin'">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminService } from '../../services/adminService'

const users = ref<any[]>([])
const loading = ref(true)

const fetchUsers = async () => {
  loading.value = true
  try {
    const data = await adminService.getUsers()
    users.value = data.data // pagination wrapper array
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const formatRole = (role: string) => {
  if (role === 'super_admin') return 'Super Admin'
  if (role === 'dokter') return 'Dokter'
  if (role === 'perawat') return 'Perawat'
  return role
}

onMounted(() => {
  fetchUsers()
})
</script>
