<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Overview Dasbor</h1>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Ringkasan aktivitas skrining dan status pasien terkini.</p>
      </div>
      <div class="flex items-center gap-2">
        <button class="px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-sm font-semibold text-slate-700 dark:text-slate-300 rounded-xl shadow-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
          Unduh Laporan
        </button>
        <button class="px-4 py-2 bg-blue-600 border border-transparent text-sm font-semibold text-white rounded-xl shadow-md shadow-blue-500/20 hover:bg-blue-700 transition-colors">
          Buat Skrining
        </button>
      </div>
    </div>

    <!-- Skeleton Loading State -->
    <div v-if="isLoading" class="space-y-8 animate-pulse">
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div v-for="i in 4" :key="i" class="h-32 rounded-2xl bg-slate-200 dark:bg-slate-800/50"></div>
      </div>
      <div class="h-96 rounded-2xl bg-slate-200 dark:bg-slate-800/50"></div>
    </div>

    <div v-else class="space-y-8">
      <!-- Metric Cards -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <div v-for="metric in metrics" :key="metric.title" 
             class="group relative overflow-hidden rounded-2xl border border-slate-200/50 dark:border-slate-700/50 bg-white/60 dark:bg-slate-900/60 backdrop-blur-xl p-6 shadow-sm transition-all duration-300 hover:-translate-y-1.5 hover:shadow-xl hover:shadow-blue-500/10 dark:hover:shadow-blue-900/20">
          <!-- Subtle Glow Background on Hover -->
          <div class="absolute -inset-px bg-gradient-to-br from-blue-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none rounded-2xl"></div>
          
          <div class="relative z-10 flex items-center justify-between pb-4">
            <h3 class="tracking-tight text-sm font-semibold text-slate-500 dark:text-slate-400">{{ metric.title }}</h3>
            <div class="text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-800 p-2 rounded-lg" v-html="metric.icon"></div>
          </div>
          <div class="relative z-10 text-3xl font-black tracking-tight text-slate-900 dark:text-white">{{ metric.value }}</div>
          
          <div class="relative z-10 flex items-center justify-between mt-2">
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 flex items-center gap-1">
              <span :class="metric.trendUp ? 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30' : 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30'" class="px-1.5 py-0.5 rounded-md flex items-center gap-0.5">
                <svg v-if="metric.trendUp" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m3 17 9-11 9 11"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m3 7 9 11 9-11"/></svg>
                {{ metric.change }}
              </span>
              <span>vs bulan lalu</span>
            </p>
          </div>
          
          <!-- Sparkline Chart -->
          <div class="relative z-10 h-10 mt-4 -mx-2 opacity-70 group-hover:opacity-100 transition-opacity">
            <v-chart class="h-full w-full" :option="getSparklineOption(metric.trendUp)" autoresize />
          </div>
        </div>
      </div>

      <!-- Table Section -->
      <div class="rounded-2xl border border-slate-200/50 dark:border-slate-700/50 bg-white/60 dark:bg-slate-900/60 backdrop-blur-xl shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20 overflow-hidden transition-all">
        <div class="p-6 pb-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <h3 class="text-lg font-bold tracking-tight text-slate-900 dark:text-white">Riwayat Skrining Terbaru</h3>
          <button class="text-sm font-semibold text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300">Lihat Semua &rarr;</button>
        </div>
        <div class="relative w-full overflow-auto">
          <table class="w-full caption-bottom text-sm">
            <thead class="[&_tr]:border-b border-slate-200/50 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/20">
              <tr class="border-b transition-colors hover:bg-slate-100/50 dark:hover:bg-slate-800/50 text-slate-500 dark:text-slate-400">
                <th class="h-12 px-6 text-left align-middle font-semibold">Pasien</th>
                <th class="h-12 px-6 text-left align-middle font-semibold">Tgl Skrining</th>
                <th class="h-12 px-6 text-left align-middle font-semibold">Usia</th>
                <th class="h-12 px-6 text-left align-middle font-semibold">Tensi (Sys/Dia)</th>
                <th class="h-12 px-6 text-left align-middle font-semibold">Tingkat Risiko</th>
                <th class="h-12 px-6 text-right align-middle font-semibold">Kepercayaan (AI)</th>
              </tr>
            </thead>
            <tbody class="[&_tr:last-child]:border-0 text-slate-700 dark:text-slate-300">
              <tr v-if="isLoading">
                <td colspan="6" class="p-6 text-center text-slate-500">Memuat data...</td>
              </tr>
              <tr v-else-if="recentScreenings.length === 0">
                <td colspan="6" class="p-6 text-center text-slate-500">Belum ada skrining.</td>
              </tr>
              <tr v-for="item in recentScreenings" :key="item.id" class="border-b border-slate-100 dark:border-slate-800/50 transition-colors hover:bg-slate-50 dark:hover:bg-slate-800/50 group">
                <td class="p-6 align-middle font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{{ item.patient?.name }}</td>
                <td class="p-6 align-middle font-medium">{{ formatDate(item.created_at) }}</td>
                <td class="p-6 align-middle">{{ item.age }} thn</td>
                <td class="p-6 align-middle font-mono text-xs font-medium">{{ item.systolic_bp }}/{{ item.diastolic_bp }} mmHg</td>
                <td class="p-6 align-middle">
                  <span 
                    class="inline-flex items-center rounded-lg px-2.5 py-1 text-xs font-bold tracking-wide shadow-sm uppercase"
                    :class="{
                      'bg-green-100 text-green-700 dark:bg-green-500/10 dark:text-green-400 ring-1 ring-inset ring-green-500/20': item.prediction?.risk_level === 'low',
                      'bg-amber-100 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400 ring-1 ring-inset ring-amber-500/20': item.prediction?.risk_level === 'medium',
                      'bg-red-100 text-red-700 dark:bg-red-500/10 dark:text-red-400 ring-1 ring-inset ring-red-500/20': item.prediction?.risk_level === 'high'
                    }"
                  >
                    <span class="w-1.5 h-1.5 rounded-full mr-1.5"
                          :class="{
                            'bg-green-500': item.prediction?.risk_level === 'low',
                            'bg-amber-500': item.prediction?.risk_level === 'medium',
                            'bg-red-500': item.prediction?.risk_level === 'high'
                          }"></span>
                    {{ item.prediction?.risk_level || 'Pending' }}
                  </span>
                </td>
                <td class="p-6 align-middle text-right font-mono font-bold">{{ item.prediction?.confidence_score ? (item.prediction.confidence_score * 100).toFixed(1) : 0 }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { dashboardService } from '../../services/dashboardService'
import { screeningService } from '../../services/screeningService'

use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

const isLoading = ref(true)
const recentScreenings = ref<any[]>([])
const statsData = ref<any>(null)

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    const [statsRes, screeningsRes] = await Promise.all([
      dashboardService.getStats(),
      screeningService.getScreenings(1)
    ])
    
    statsData.value = statsRes
    recentScreenings.value = screeningsRes.data.slice(0, 5) // ambil 5 terbaru
    
    updateMetrics()
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('id-ID', {
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => {
  fetchDashboardData()
})

const metrics = ref<any[]>([])

const updateMetrics = () => {
  if (!statsData.value) return
  
  metrics.value = [
    {
      title: 'Total Skrining',
      value: statsData.value.total_screenings,
      change: '100%',
      trendUp: true,
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
    },
    {
      title: 'Risiko Tinggi Terdeteksi',
      value: statsData.value.high_risk_count,
      change: statsData.value.high_risk_percentage + '%',
      trendUp: false,
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>'
    },
    {
      title: 'Total Pasien Terdaftar',
      value: statsData.value.total_patients,
      change: '100%',
      trendUp: true,
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>'
    },
    {
      title: 'Risiko Rendah (Aman)',
      value: statsData.value.low_risk_count,
      change: statsData.value.low_risk_percentage + '%',
      trendUp: true,
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'
    }
  ]
}

const getSparklineOption = (trendUp: boolean) => {
  const color = trendUp ? '#10b981' : '#f43f5e' // emerald-500 or rose-500
  // Randomize data slightly based on trend for visual effect
  const baseData = trendUp ? [10, 15, 12, 18, 24, 20, 30] : [30, 25, 28, 20, 15, 18, 10]
  const data = baseData.map(v => v + (Math.random() * 5 - 2.5))
  
  return {
    grid: { left: 0, right: 0, top: 2, bottom: 2 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, min: 0 },
    series: [
      {
        data,
        type: 'line',
        smooth: 0.4,
        symbol: 'none',
        lineStyle: { width: 2, color },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: color + '30' }, // 30% opacity
              { offset: 1, color: color + '00' }  // 0% opacity
            ]
          }
        }
      }
    ]
  }
}
</script>
