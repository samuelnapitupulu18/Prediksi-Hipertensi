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

const isLoading = ref(true)

// Mocked Data from ML Engine Response Schema
const predictionData = ref({
  risk_level: 'high',
  confidence_score: 0.89,
  probability: { low: 0.05, medium: 0.06, high: 0.89 },
  inference_time_ms: 12.4,
  feature_importance: [
    { feature: 'systolic_bp', importance: 0.35 },
    { feature: 'age', importance: 0.20 },
    { feature: 'bmi', importance: 0.15 },
    { feature: 'diastolic_bp', importance: 0.12 },
    { feature: 'cholesterol_level', importance: 0.08 },
    { feature: 'smoking_status', importance: 0.05 }
  ]
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
      data: sortedFI.map(f => f.feature.toUpperCase().replace('_', ' ')),
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

onMounted(() => {
  // Simulate network delay
  setTimeout(() => {
    isLoading.value = false
  }, 1200)
})
</script>
