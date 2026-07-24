<template>
  <div class="space-y-6 max-w-6xl mx-auto pb-12">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">
        Perbandingan Model
      </h1>
      <p class="mt-1 text-sm text-slate-500 dark:text-slate-400 max-w-3xl">
        Seluruh angka pada halaman ini dibaca dari metadata model yang sedang dipakai
        sistem — hasil pengukuran saat pelatihan, bukan nilai yang dituliskan di
        antarmuka.
      </p>
    </div>

    <div v-if="loading" class="rounded-2xl bg-white dark:bg-slate-900 p-10 ring-1 ring-slate-200 dark:ring-slate-800 text-center">
      <p class="text-sm text-slate-500 dark:text-slate-400">Memuat metadata model…</p>
    </div>

    <div v-else-if="error" class="rounded-2xl border border-red-200 dark:border-red-800/50 bg-red-50 dark:bg-red-950/30 p-5">
      <p class="text-sm font-medium text-red-700 dark:text-red-300">{{ error }}</p>
      <p class="text-xs text-red-600 dark:text-red-400 mt-2">
        Pastikan ML Engine berjalan dan model produksi sudah dilatih:
        <span class="font-mono">python scripts/train_production_model.py</span>
      </p>
    </div>

    <template v-else-if="info">
      <!-- Identitas model -->
      <div class="rounded-2xl bg-white dark:bg-slate-900 p-6 ring-1 ring-slate-200 dark:ring-slate-800">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-5">
          <div>
            <p class="text-xs font-bold text-slate-500 dark:text-slate-400">Versi Model</p>
            <p class="mt-1 font-mono font-bold text-slate-900 dark:text-white">{{ info.version }}</p>
          </div>
          <div>
            <p class="text-xs font-bold text-slate-500 dark:text-slate-400">Algoritma</p>
            <p class="mt-1 font-bold text-slate-900 dark:text-white">{{ info.algorithm }}</p>
          </div>
          <div>
            <p class="text-xs font-bold text-slate-500 dark:text-slate-400">Optimasi</p>
            <p class="mt-1 font-bold text-slate-900 dark:text-white">{{ info.optimization }}</p>
          </div>
          <div>
            <p class="text-xs font-bold text-slate-500 dark:text-slate-400">Dilatih Pada</p>
            <p class="mt-1 font-mono text-sm text-slate-900 dark:text-white">{{ info.trained_at || '—' }}</p>
          </div>
        </div>

        <div v-if="info.dataset" class="mt-5 pt-5 border-t border-slate-100 dark:border-slate-800">
          <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
            Dataset <span class="font-mono">{{ info.dataset.file }}</span> —
            {{ info.dataset.total_samples?.toLocaleString('id-ID') }} sampel
            ({{ info.dataset.split?.train }} latih / {{ info.dataset.split?.validation }} validasi /
            {{ info.dataset.split?.test }} uji).
            Tugas: <span class="font-mono">{{ info.task }}</span>.
          </p>
        </div>
      </div>

      <!-- Metrik nyata -->
      <div class="rounded-2xl bg-white dark:bg-slate-900 ring-1 ring-slate-200 dark:ring-slate-800 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800">
          <h2 class="text-sm font-bold text-slate-900 dark:text-white">Metrik pada Data Uji</h2>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Diukur pada data yang tidak dipakai selama pelatihan maupun optimasi
          </p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-5 divide-x divide-slate-100 dark:divide-slate-800">
          <div v-for="m in metrikUtama" :key="m.key" class="p-5">
            <p class="text-[11px] font-bold text-slate-500 dark:text-slate-400">{{ m.label }}</p>
            <p class="mt-1 text-2xl font-extrabold text-slate-900 dark:text-white">
              {{ m.value }}<span class="text-sm">%</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Hyperparameter & proses pencarian -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div class="rounded-2xl bg-white dark:bg-slate-900 ring-1 ring-slate-200 dark:ring-slate-800 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800">
            <h2 class="text-sm font-bold text-slate-900 dark:text-white">Hyperparameter Terpakai</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Ditemukan algoritma SGO saat pelatihan</p>
          </div>
          <table class="w-full text-sm">
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="(v, k) in info.hyperparameters" :key="k">
                <td class="px-6 py-3 font-mono text-xs text-slate-600 dark:text-slate-400">{{ k }}</td>
                <td class="px-6 py-3 text-right font-mono font-bold text-slate-900 dark:text-white">{{ v }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="pencarian.length" class="rounded-2xl bg-white dark:bg-slate-900 ring-1 ring-slate-200 dark:ring-slate-800 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800">
            <h2 class="text-sm font-bold text-slate-900 dark:text-white">Proses Pencarian</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Catatan optimasi yang benar-benar dijalankan</p>
          </div>
          <table class="w-full text-sm">
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="row in pencarian" :key="row.label">
                <td class="px-6 py-3 text-xs text-slate-600 dark:text-slate-400">{{ row.label }}</td>
                <td class="px-6 py-3 text-right font-mono font-bold text-slate-900 dark:text-white">{{ row.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Kepentingan fitur -->
      <div class="rounded-2xl bg-white dark:bg-slate-900 p-6 ring-1 ring-slate-200 dark:ring-slate-800">
        <h2 class="text-sm font-bold text-slate-900 dark:text-white">Kepentingan Fitur</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">
          Dihitung dari model dengan metode <span class="font-mono">gain</span>, dinormalisasi
        </p>
        <v-chart class="w-full" :style="{ height: tinggiGrafik }" :option="opsiKepentingan" autoresize />

        <div v-if="fiturNol.length" class="mt-4 p-4 rounded-xl bg-amber-50 dark:bg-amber-900/20 ring-1 ring-amber-200 dark:ring-amber-800/50">
          <p class="text-xs font-bold text-amber-800 dark:text-amber-300">
            {{ fiturNol.length }} fitur tidak berkontribusi sama sekali (gain = 0)
          </p>
          <p class="text-xs text-amber-700 dark:text-amber-400 mt-1 leading-relaxed">
            {{ fiturNol.join(', ') }}. Model hanya bertumpu pada tekanan darah karena label
            pada dataset memang ditentukan dari ambang TDS/TDD. Ini keterbatasan dataset,
            bukan kesalahan pemodelan — dan justru inilah yang berhasil diungkap oleh
            analisis XAI.
          </p>
        </div>
      </div>

      <!-- Catatan metodologi -->
      <div v-if="info.notes?.length" class="rounded-2xl bg-slate-50 dark:bg-slate-800/50 p-5 ring-1 ring-slate-200 dark:ring-slate-700">
        <p class="text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">Catatan Metodologi</p>
        <ul class="space-y-1.5">
          <li v-for="(n, i) in info.notes" :key="i" class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed flex gap-2">
            <span class="text-slate-400">•</span><span>{{ n }}</span>
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { TooltipComponent, GridComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { optimizationService } from '../../services/optimizationService'

use([CanvasRenderer, BarChart, TooltipComponent, GridComponent])

const loading = ref(true)
const error = ref('')
const info = ref<any>(null)

const metrikUtama = computed(() => {
  const m = info.value?.metrics_test_set
  if (!m) return []
  return [
    { key: 'accuracy', label: 'Accuracy', value: m.accuracy },
    { key: 'precision', label: 'Precision (macro)', value: m.precision_macro },
    { key: 'recall', label: 'Recall (macro)', value: m.recall_macro },
    { key: 'f1', label: 'F1-Score (macro)', value: m.f1_macro },
    { key: 'auc', label: 'AUC', value: m.auc },
  ].filter((r) => r.value !== undefined && r.value !== null)
})

const pencarian = computed(() => {
  const s = info.value?.hyperparameter_search
  if (!s) return []
  return [
    { label: 'Metode', value: s.method },
    { label: 'Iterasi', value: s.iterations },
    { label: 'Ukuran populasi', value: s.population_size },
    { label: 'Fungsi fitness', value: s.fitness },
    { label: 'Fitness terbaik (validasi)', value: `${s.best_validation_fitness}%` },
    { label: 'Jumlah pelatihan model', value: s.model_trainings },
    { label: 'Lama optimasi', value: `${s.optimization_seconds} s` },
  ].filter((r) => r.value !== undefined && r.value !== null)
})

const kepentingan = computed<any[]>(() => info.value?.feature_importance ?? [])

const fiturNol = computed(() =>
  kepentingan.value.filter((f) => Number(f.importance) === 0).map((f) => f.label || f.feature)
)

const tinggiGrafik = computed(() => `${Math.max(kepentingan.value.length * 34, 200)}px`)

const opsiKepentingan = computed(() => {
  const data = [...kepentingan.value].reverse()
  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: 210, right: 60, top: 10, bottom: 25 },
    xAxis: { type: 'value', axisLabel: { color: '#94a3b8' } },
    yAxis: {
      type: 'category',
      data: data.map((f: any) => f.label || f.feature),
      axisLabel: { color: '#94a3b8', fontSize: 11 },
    },
    series: [
      {
        type: 'bar',
        data: data.map((f: any) => Number(f.importance)),
        itemStyle: { color: '#3b82f6', borderRadius: [0, 4, 4, 0] },
        label: {
          show: true,
          position: 'right',
          formatter: (v: any) => Number(v.data).toFixed(4),
          color: '#94a3b8',
          fontSize: 10,
        },
      },
    ],
  }
})

onMounted(async () => {
  try {
    info.value = await optimizationService.modelInfo()
  } catch (e: any) {
    error.value = e?.response?.data?.message || 'Gagal memuat metadata model dari ML Engine.'
  } finally {
    loading.value = false
  }
})
</script>
