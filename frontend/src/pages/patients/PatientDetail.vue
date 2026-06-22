<template>
  <div class="space-y-6" v-if="patient">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <router-link :to="{ name: 'patient-list' }" class="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-600 dark:text-slate-300"><path d="m15 18-6-6 6-6"/></svg>
        </router-link>
        <h1 class="text-2xl font-bold text-slate-800 dark:text-white">Detail Pasien</h1>
      </div>
      <router-link :to="{ name: 'screening-new', query: { nik: patient.nik, name: patient.name, dob: patient.date_of_birth, gender: patient.gender } }" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
        + Skrining Baru
      </router-link>
    </div>

    <!-- Identitas Pasien -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div>
          <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Nama Pasien</p>
          <p class="text-lg font-semibold text-slate-900 dark:text-white mt-1">{{ patient.name }}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500 dark:text-slate-400">NIK</p>
          <p class="text-lg font-mono font-medium text-slate-900 dark:text-white mt-1">{{ patient.nik }}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Tanggal Lahir / Usia</p>
          <p class="text-lg font-medium text-slate-900 dark:text-white mt-1">{{ patient.date_of_birth }} ({{ calculateAge(patient.date_of_birth) }} Thn)</p>
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Jenis Kelamin</p>
          <p class="text-lg font-medium text-slate-900 dark:text-white mt-1">{{ patient.gender === 'male' ? 'Laki-laki' : 'Perempuan' }}</p>
        </div>
      </div>
    </div>

    <!-- Riwayat Skrining -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6">
      <h2 class="text-lg font-bold text-slate-800 dark:text-white mb-4">Riwayat Skrining</h2>
      
      <div v-if="patient.screenings?.length === 0" class="text-center py-8 text-slate-500 dark:text-slate-400 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl">
        Belum ada riwayat skrining untuk pasien ini.
      </div>
      
      <div v-else class="space-y-4">
        <div v-for="screening in patient.screenings" :key="screening.id" class="border border-slate-200 dark:border-slate-700 rounded-xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 hover:border-blue-300 dark:hover:border-blue-700 transition-colors">
          <div class="flex flex-col gap-1">
            <span class="text-sm font-medium text-slate-500 dark:text-slate-400">{{ formatDate(screening.created_at) }}</span>
            <div class="flex items-center gap-2">
              <span class="font-semibold text-slate-800 dark:text-white">Hasil Prediksi:</span>
              <span :class="getRiskBadgeColor(screening.prediction?.risk_level)" class="px-2 py-1 text-xs font-bold rounded-md uppercase">
                {{ screening.prediction?.risk_level || 'Pending' }}
              </span>
            </div>
            <p class="text-xs text-slate-500 mt-1">Tekanan Darah: {{ screening.systolic_bp }}/{{ screening.diastolic_bp }} | BMI: {{ screening.bmi }}</p>
          </div>
          
          <router-link :to="{ name: 'screening-result', params: { id: screening.id } }" class="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 font-medium text-sm flex items-center gap-1">
            Lihat Laporan Lengkap
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </router-link>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="flex justify-center py-20">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { patientService } from '../../services/patientService'

const route = useRoute()
const patient = ref<any>(null)
const loading = ref(true)

const fetchPatientData = async () => {
  loading.value = true
  try {
    patient.value = await patientService.getPatient(Number(route.params.id))
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const calculateAge = (dob: string) => {
  const diff = Date.now() - new Date(dob).getTime()
  const age = new Date(diff)
  return Math.abs(age.getUTCFullYear() - 1970)
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
  fetchPatientData()
})
</script>
