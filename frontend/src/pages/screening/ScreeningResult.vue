<template>
  <div class="space-y-6" v-if="screening">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button @click="router.back()" class="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-600 dark:text-slate-300"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <h1 class="text-2xl font-bold text-slate-800 dark:text-white">Hasil Skrining</h1>
      </div>
      <button @click="downloadPDF" :disabled="downloading" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2">
        <svg v-if="downloading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
        {{ downloading ? 'Mempersiapkan...' : 'Unduh PDF' }}
      </button>
    </div>

    <!-- Area yang akan dirender PDF -->
    <div id="pdf-content" class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 p-8 space-y-8">
      
      <!-- Header Laporan -->
      <div class="border-b border-slate-200 dark:border-slate-700 pb-6 flex justify-between items-start">
        <div>
          <h2 class="text-2xl font-black text-slate-900 dark:text-white">Laporan Deteksi Dini PJK</h2>
          <p class="text-slate-500 mt-1">Sistem Cerdas berbasis AI</p>
        </div>
        <div class="text-right">
          <p class="text-sm text-slate-500">Tanggal Pemeriksaan:</p>
          <p class="font-medium text-slate-900 dark:text-white">{{ formatDate(screening.created_at) }}</p>
        </div>
      </div>

      <!-- Informasi Pasien & Hasil -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="space-y-4">
          <h3 class="text-lg font-bold text-slate-800 dark:text-white border-b border-slate-100 dark:border-slate-700 pb-2">Data Pasien</h3>
          <div class="grid grid-cols-2 gap-y-3 text-sm">
            <div class="text-slate-500">NIK:</div>
            <div class="font-medium text-slate-900 dark:text-white">{{ screening.patient?.nik }}</div>
            <div class="text-slate-500">Nama:</div>
            <div class="font-medium text-slate-900 dark:text-white">{{ screening.patient?.name }}</div>
            <div class="text-slate-500">Usia:</div>
            <div class="font-medium text-slate-900 dark:text-white">{{ screening.age }} Tahun</div>
            <div class="text-slate-500">Jenis Kelamin:</div>
            <div class="font-medium text-slate-900 dark:text-white">{{ screening.gender === 'male' ? 'Laki-laki' : 'Perempuan' }}</div>
            <div class="text-slate-500">BMI:</div>
            <div class="font-medium text-slate-900 dark:text-white">{{ screening.bmi }}</div>
            <div class="text-slate-500">Tekanan Darah:</div>
            <div class="font-medium text-slate-900 dark:text-white">{{ screening.systolic_bp }} / {{ screening.diastolic_bp }} mmHg</div>
          </div>
        </div>

        <div class="space-y-4">
          <h3 class="text-lg font-bold text-slate-800 dark:text-white border-b border-slate-100 dark:border-slate-700 pb-2">Hasil Prediksi AI</h3>
          <div class="bg-slate-50 dark:bg-slate-900/50 rounded-xl p-4 border border-slate-200 dark:border-slate-700">
            <div class="flex items-center justify-between mb-4">
              <span class="text-sm font-medium text-slate-600 dark:text-slate-400">Tingkat Risiko:</span>
              <span :class="getRiskBadgeColor(screening.prediction?.risk_level)" class="px-3 py-1 rounded-lg font-bold uppercase tracking-wider text-sm">
                {{ screening.prediction?.risk_level }}
              </span>
            </div>
            
            <div class="space-y-2">
              <div class="flex justify-between text-xs text-slate-500">
                <span>Tingkat Kepercayaan Model</span>
                <span>{{ (screening.prediction?.confidence_score * 100).toFixed(1) }}%</span>
              </div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                <div class="h-2 rounded-full" :class="getConfidenceColor(screening.prediction?.risk_level)" :style="{ width: `${screening.prediction?.confidence_score * 100}%` }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Feature Importance (XAI) -->
      <div v-if="screening.prediction?.feature_importance">
        <h3 class="text-lg font-bold text-slate-800 dark:text-white border-b border-slate-100 dark:border-slate-700 pb-2 mb-4">Faktor Kontribusi Utama (Explainable AI)</h3>
        <p class="text-sm text-slate-500 mb-4">Faktor-faktor berikut merupakan metrik yang paling mempengaruhi hasil prediksi risiko pada pasien ini berdasarkan analisis model AI.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="(feature, index) in topFeatures" :key="index" class="flex items-center gap-4">
            <div class="w-1/3 text-sm font-medium text-slate-700 dark:text-slate-300 truncate" :title="feature.label">{{ feature.label }}</div>
            <div class="w-2/3 flex items-center gap-2">
              <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2.5">
                <div class="bg-blue-500 h-2.5 rounded-full" :style="{ width: `${Math.min(Math.abs(feature.importance) * 200, 100)}%` }"></div>
              </div>
              <span class="text-xs text-slate-500 font-mono w-10">{{ (feature.importance).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Footer Laporan -->
      <div class="pt-8 mt-8 border-t border-slate-200 dark:border-slate-700 text-center">
        <p class="text-xs text-slate-400">
          *Laporan ini dihasilkan oleh AI berdasarkan data skrining yang dimasukkan. <br/>
          Harap konsultasikan hasil ini dengan dokter untuk diagnosis lebih lanjut.
        </p>
      </div>

    </div>
  </div>
  <div v-else class="flex justify-center py-20">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { screeningService } from '../../services/screeningService'

// Dynamic import html2pdf so it doesn't break SSR (though this is SPA, it's safer)
let html2pdf: any;
if (typeof window !== 'undefined') {
  import('html2pdf.js').then(module => {
    html2pdf = module.default;
  });
}

const route = useRoute()
const router = useRouter()
const screening = ref<any>(null)
const downloading = ref(false)

const fetchScreening = async () => {
  try {
    const response = await screeningService.getScreening(Number(route.params.id))
    screening.value = response.data
  } catch (e) {
    console.error(e)
  }
}

const topFeatures = computed(() => {
  if (!screening.value?.prediction?.feature_importance) return []
  return [...screening.value.prediction.feature_importance]
    .sort((a: any, b: any) => Math.abs(b.importance) - Math.abs(a.importance))
    .slice(0, 6)
})

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

const getConfidenceColor = (level: string) => {
  if (level === 'high') return 'bg-red-500'
  if (level === 'medium') return 'bg-orange-500'
  if (level === 'low') return 'bg-green-500'
  return 'bg-blue-500'
}

const downloadPDF = async () => {
  if (!html2pdf) {
    alert('Modul PDF sedang dimuat, silakan coba lagi dalam beberapa detik.');
    return;
  }
  
  downloading.value = true
  try {
    const element = document.getElementById('pdf-content')
    const opt = {
      margin:       [10, 10, 10, 10],
      filename:     `Laporan-Skrining-${screening.value.patient?.nik}.pdf`,
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2, useCORS: true, logging: false },
      jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }
    
    // For dark mode compatibility when printing, temporarily enforce light mode classes or just let it print dark
    await html2pdf().set(opt).from(element).save()
  } catch (error) {
    console.error("Failed to generate PDF", error)
  } finally {
    downloading.value = false
  }
}

onMounted(() => {
  fetchScreening()
})
</script>
