<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-slate-900">Explainable AI (XAI) Dashboard</h1>
        <p class="text-sm text-slate-500">Transparansi pengambilan keputusan dari model XGBoost (SGO Optimized).</p>
      </div>
      <div class="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-semibold rounded-full border border-blue-200">
        Model v1.0.0-sgo
      </div>
    </div>

    <!-- Skeleton Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-3 gap-6 animate-pulse">
      <div class="col-span-1 h-64 bg-slate-200 rounded-xl border border-slate-100"></div>
      <div class="col-span-2 h-64 bg-slate-200 rounded-xl border border-slate-100"></div>
      <div class="col-span-3 h-80 bg-slate-200 rounded-xl border border-slate-100"></div>
    </div>

    <!-- Empty State: belum ada skrining -->
    <div v-else-if="!hasData" class="flex flex-col items-center justify-center py-20 gap-4 text-center rounded-xl border border-dashed border-slate-300 bg-white">
      <div class="h-16 w-16 rounded-2xl bg-blue-50 flex items-center justify-center text-3xl">🤖</div>
      <p class="text-sm font-medium text-slate-600 max-w-sm">Belum ada data skrining untuk dianalisis. Lakukan skrining terlebih dahulu, lalu hasil prediksi model akan tampil di sini.</p>
      <router-link :to="{ name: 'screening-new' }" class="px-5 py-2.5 text-sm font-bold text-white bg-blue-600 rounded-xl hover:bg-blue-700 transition-all active:scale-95">Mulai Skrining</router-link>
    </div>

    <!-- Bento Box Grid Layout -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Prediction Summary (Gauge Chart) -->
      <div class="col-span-1 rounded-xl border border-slate-200 bg-white p-6 shadow-sm flex flex-col items-center justify-center relative overflow-hidden">
        <div class="absolute top-4 left-4 flex items-center gap-2">
          <div class="h-2 w-2 rounded-full bg-red-500 animate-pulse"></div>
          <span class="text-xs font-medium text-slate-500">LIVE PREDICTION</span>
        </div>
        
        <h3 class="mt-4 text-sm font-medium text-slate-500 uppercase tracking-wider">Risiko Hipertensi</h3>
        <v-chart class="h-48 w-full mt-2" :option="gaugeOption" autoresize />
        
        <div class="text-center mt-2">
          <p class="text-3xl font-extrabold" :class="riskColor">{{ predictionData.risk_level.toUpperCase() }}</p>
          <p class="text-sm text-slate-500 mt-1">Confidence Score: {{ (predictionData.confidence_score * 100).toFixed(1) }}%</p>
          <p v-if="latestPatientName" class="text-xs text-slate-400 mt-1">Skrining terakhir: {{ latestPatientName }}</p>
        </div>
      </div>

      <!-- Feature Importance (Horizontal Bar Chart) -->
      <div class="col-span-2 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 class="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">Feature Importance (SHAP/Gain)</h3>
        <v-chart class="h-64 w-full" :option="barOption" autoresize />
      </div>

      <!-- Detail Probabilities Bento -->
      <div class="col-span-1 md:col-span-3 rounded-xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
        <h3 class="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">Distribusi Probabilitas Kelas</h3>
        <div class="grid grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded-lg border border-slate-200 text-center">
            <p class="text-xs text-slate-500 font-semibold mb-1">Rendah (Low)</p>
            <p class="text-xl font-bold text-green-600">{{ (predictionData.probability.low * 100).toFixed(1) }}%</p>
          </div>
          <div class="bg-white p-4 rounded-lg border border-slate-200 text-center">
            <p class="text-xs text-slate-500 font-semibold mb-1">Sedang (Medium)</p>
            <p class="text-xl font-bold text-yellow-600">{{ (predictionData.probability.medium * 100).toFixed(1) }}%</p>
          </div>
          <div class="bg-white p-4 rounded-lg border border-slate-200 text-center">
            <p class="text-xs text-slate-500 font-semibold mb-1">Tinggi (High)</p>
            <p class="text-xl font-bold text-red-600">{{ (predictionData.probability.high * 100).toFixed(1) }}%</p>
          </div>
        </div>
        <p class="text-xs text-slate-400 mt-4 text-center">Inference Time: {{ predictionData.inference_time_ms }}ms via FastAPI</p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { GaugeChart, BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
import VChart from 'vue-echarts'

// Register ECharts modules
use([CanvasRenderer, GaugeChart, BarChart, TitleComponent, TooltipComponent, GridComponent])

import { screeningService } from '../../services/screeningService'

const isLoading = ref(true)
const hasData = ref(true)
const latestPatientName = ref('')

// Diisi dari prediksi skrining terbaru (API backend / penyimpanan lokal)
const predictionData = ref({
  risk_level: 'low',
  confidence_score: 0,
  probability: { low: 0, medium: 0, high: 0 },
  inference_time_ms: 0,
  feature_importance: [] as { feature: string; importance: number; label?: string }[]
})

const riskColor = computed(() => {
  if (predictionData.value.risk_level === 'high') return 'text-red-600'
  if (predictionData.value.risk_level === 'medium') return 'text-yellow-600'
  return 'text-green-600'
})

// ECharts Gauge Configuration
const gaugeOption = computed(() => ({
  series: [
    {
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 100,
      splitNumber: 10,
      axisLine: {
        lineStyle: {
          width: 10,
          color: [
            [0.3, '#16a34a'], // Green
            [0.7, '#ca8a04'], // Yellow
            [1, '#dc2626']    // Red
          ]
        }
      },
      pointer: { icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z', length: '12%', width: 10, offsetCenter: [0, '-60%'] },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      detail: { show: false },
      data: [{ value: predictionData.value.confidence_score * 100 }]
    }
  ]
}))

// ECharts Bar Configuration
const barOption = computed(() => {
  // Sort reverse for horizontal bar chart (highest on top)
  const sortedFI = [...predictionData.value.feature_importance].reverse()
  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '5%', containLabel: true },
    xAxis: { type: 'value', show: false },
    yAxis: { 
      type: 'category', 
      // Pakai label Bahasa Indonesia dari ML Engine; kode fitur hanya cadangan
      data: sortedFI.map(f => f.label || f.feature.toUpperCase().replace(/_/g, ' ')),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#64748b', fontSize: 11, fontWeight: 'bold' }
    },
    series: [
      {
        type: 'bar',
        data: sortedFI.map(f => f.importance),
        itemStyle: { color: '#3b82f6', borderRadius: [0, 4, 4, 0] },
        barWidth: '60%',
        label: { show: true, position: 'right', formatter: (val: any) => val.data.toFixed(3), color: '#94a3b8', fontSize: 10 }
      }
    ]
  }
})

onMounted(async () => {
  try {
    const res: any = await screeningService.getScreenings(1)
    const latest = res.data?.[0]
    if (latest?.prediction) {
      const p = latest.prediction
      predictionData.value = {
        risk_level: p.risk_level || 'low',
        confidence_score: Number(p.confidence_score || 0),
        probability: { low: 0, medium: 0, high: 0, ...(p.probability_distribution || p.probability || {}) },
        inference_time_ms: Number(p.inference_time_ms || 0),
        feature_importance: p.feature_importance || []
      }
      latestPatientName.value = latest.patient?.name || latest.name || ''
    } else {
      hasData.value = false
    }
  } catch (e) {
    console.warn('Gagal memuat data XAI', e)
    hasData.value = false
  } finally {
    isLoading.value = false
  }
})
</script>
