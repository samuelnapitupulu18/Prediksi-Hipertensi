<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-slate-800 dark:text-white">Audit Log Aktivitas</h1>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-600 dark:text-slate-300">
          <thead class="bg-slate-50 dark:bg-slate-900/50 text-slate-500 dark:text-slate-400 font-medium border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="px-6 py-4">Waktu</th>
              <th class="px-6 py-4">Pengguna</th>
              <th class="px-6 py-4">Aksi</th>
              <th class="px-6 py-4">Deskripsi</th>
              <th class="px-6 py-4">IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="animate-pulse">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">Memuat log...</td>
            </tr>
            <tr v-else-if="logs.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">Belum ada aktivitas tercatat.</td>
            </tr>
            <tr v-for="log in logs" :key="log.id" class="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
              <td class="px-6 py-4 font-mono text-xs">{{ formatDate(log.created_at) }}</td>
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">
                {{ log.user?.name || 'Sistem' }}
                <span v-if="log.user?.role" class="ml-2 text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400">{{ log.user.role }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="px-2 py-1 bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400 rounded text-xs font-mono border border-blue-100 dark:border-blue-800">{{ log.action }}</span>
              </td>
              <td class="px-6 py-4">{{ log.description }}</td>
              <td class="px-6 py-4 text-xs font-mono text-slate-400">{{ log.ip_address }}</td>
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

const logs = ref<any[]>([])
const loading = ref(true)

const fetchLogs = async () => {
  loading.value = true
  try {
    const data = await adminService.getAuditLogs()
    logs.value = data.data // pagination wrapper array
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  fetchLogs()
})
</script>
