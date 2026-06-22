<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-slate-800 dark:text-white">Riwayat Skrining</h1>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-600 dark:text-slate-300">
          <thead class="bg-slate-50 dark:bg-slate-900/50 text-slate-500 dark:text-slate-400 font-medium border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="px-6 py-4">Tanggal & Waktu</th>
              <th class="px-6 py-4">Nama Pasien</th>
              <th class="px-6 py-4">Risiko Prediksi</th>
              <th class="px-6 py-4">Confidence</th>
              <th class="px-6 py-4 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="animate-pulse">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">Memuat data...</td>
            </tr>
            <tr v-else-if="screenings.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">Belum ada riwayat skrining.</td>
            </tr>
            <tr v-for="screening in screenings" :key="screening.id" class="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
              <td class="px-6 py-4">{{ formatDate(screening.created_at) }}</td>
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">{{ screening.patient?.name }}</td>
              <td class="px-6 py-4">
                <span :class="getRiskBadgeColor(screening.prediction?.risk_level)" class="px-2 py-1 text-xs font-bold rounded-md uppercase">
                  {{ screening.prediction?.risk_level || 'Pending' }}
                </span>
              </td>
              <td class="px-6 py-4">{{ (screening.prediction?.confidence_score * 100).toFixed(1) }}%</td>
              <td class="px-6 py-4 text-right">
                <router-link :to="{ name: 'screening-result', params: { id: screening.id } }" class="text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium">
                  Lihat Detail
                </router-link>
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
import { screeningService } from '../../services/screeningService'

const screenings = ref<any[]>([])
const loading = ref(true)

const fetchScreenings = async () => {
  loading.value = true
  try {
    const data = await screeningService.getScreenings()
    screenings.value = data.data // pagination wrapper
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
    minute: '2-digit'
  })
}

const getRiskBadgeColor = (level: string) => {
  if (level === 'high') return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
  if (level === 'medium') return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
  if (level === 'low') return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
  return 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-400'
}

onMounted(() => {
  fetchScreenings()
})
</script>
