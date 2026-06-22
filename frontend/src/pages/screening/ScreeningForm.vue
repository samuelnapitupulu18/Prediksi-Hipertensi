<template>
  <div class="mx-auto max-w-3xl space-y-8">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Skrining Klinis</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Evaluasi 11 atribut risiko hipertensi dengan model prediksi XGBoost.</p>
      </div>
      <div class="flex items-center gap-2 bg-blue-50 dark:bg-blue-900/30 px-3 py-1.5 rounded-full border border-blue-100 dark:border-blue-800">
        <span class="text-sm font-bold text-blue-700 dark:text-blue-400">Langkah {{ step }} dari 3</span>
      </div>
    </div>

    <!-- Sticky Progress Bar with Glow -->
    <div class="sticky top-20 z-10 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md py-4 -mx-4 px-4 sm:mx-0 sm:px-0 transition-colors">
      <div class="w-full bg-slate-100 dark:bg-slate-800 h-3 rounded-full overflow-hidden shadow-inner relative">
        <div class="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500 ease-out shadow-[0_0_10px_rgba(79,70,229,0.5)]" :style="{ width: `${(step / 3) * 100}%` }"></div>
      </div>
    </div>

    <!-- Form Container -->
    <div class="rounded-3xl border border-slate-200/50 dark:border-slate-800/50 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl p-6 sm:p-10 shadow-xl shadow-slate-200/40 dark:shadow-slate-900/40 transition-colors">
      <form @submit.prevent="onSubmit" :class="{ 'animate-shake': formErrors }">
        
        <!-- STEP 1: Demografi & Antropometri -->
        <div v-show="step === 1" class="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
          <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-10 w-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">1</div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">Demografi & Fisik</h3>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Identitas -->
            <div class="md:col-span-2 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">NIK (Nomor Induk Kependudukan)</label>
              <input type="text" v-model="formData.nik" class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="16 digit NIK" maxlength="16" />
              <p v-if="errors.nik" class="text-xs font-medium text-red-500">{{ errors.nik }}</p>
            </div>

            <div class="md:col-span-2 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Nama Lengkap</label>
              <input type="text" v-model="formData.name" class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Nama sesuai KTP" />
              <p v-if="errors.name" class="text-xs font-medium text-red-500">{{ errors.name }}</p>
            </div>
            
            <div class="md:col-span-1 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Tanggal Lahir</label>
              <input type="date" v-model="formData.date_of_birth" class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-blue-500 outline-none" />
              <p v-if="errors.date_of_birth" class="text-xs font-medium text-red-500">{{ errors.date_of_birth }}</p>
            </div>

            <!-- Usia -->
            <div class="md:col-span-1 space-y-3">
              <label class="flex items-center justify-between text-sm font-bold text-slate-700 dark:text-slate-300">
                <span>Usia (Tahun)</span>
                <span class="text-xl font-black text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 px-3 py-1 rounded-lg border border-blue-100 dark:border-blue-800">{{ formData.age }}</span>
              </label>
              <div class="pt-2">
                <input type="range" v-model.number="formData.age" min="18" max="100" class="w-full accent-blue-600 dark:accent-blue-500" />
              </div>
              <p v-if="errors.age" class="text-xs font-medium text-red-500 animate-in slide-in-from-top-1">{{ errors.age }}</p>
            </div>

            <!-- Jenis Kelamin -->
            <div class="md:col-span-1 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Jenis Kelamin</label>
              <div class="grid grid-cols-2 gap-3">
                <label class="relative cursor-pointer">
                  <input type="radio" v-model="formData.gender" value="male" class="peer sr-only" name="gender" />
                  <div class="rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 text-center transition-all peer-checked:border-blue-600 peer-checked:bg-blue-50 dark:peer-checked:bg-blue-900/20 peer-checked:text-blue-700 dark:peer-checked:text-blue-400 hover:bg-slate-50 dark:hover:bg-slate-700/50">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><circle cx="10" cy="10" r="6"/><path d="m14 14 7 7"/><path d="m14 21 7-7"/></svg>
                    <span class="font-semibold text-sm">Laki-laki</span>
                  </div>
                </label>
                <label class="relative cursor-pointer">
                  <input type="radio" v-model="formData.gender" value="female" class="peer sr-only" name="gender" />
                  <div class="rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 text-center transition-all peer-checked:border-pink-500 peer-checked:bg-pink-50 dark:peer-checked:bg-pink-900/20 peer-checked:text-pink-600 dark:peer-checked:text-pink-400 hover:bg-slate-50 dark:hover:bg-slate-700/50">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><circle cx="12" cy="10" r="6"/><path d="M12 16v6"/><path d="M9 19h6"/></svg>
                    <span class="font-semibold text-sm">Perempuan</span>
                  </div>
                </label>
              </div>
              <p v-if="errors.gender" class="text-xs font-medium text-red-500 animate-in slide-in-from-top-1">{{ errors.gender }}</p>
            </div>

            <!-- BMI -->
            <div class="md:col-span-2 space-y-3">
              <label class="flex items-center justify-between text-sm font-bold text-slate-700 dark:text-slate-300">
                <span>Body Mass Index (BMI)</span>
                <span class="text-xl font-black text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 px-3 py-1 rounded-lg border border-blue-100 dark:border-blue-800">{{ formData.bmi }}</span>
              </label>
              <div class="pt-2">
                <input type="range" v-model.number="formData.bmi" min="10" max="60" step="0.1" class="w-full accent-blue-600 dark:accent-blue-500" />
              </div>
              <div class="flex justify-between text-xs font-medium text-slate-400">
                <span>Underweight</span>
                <span>Normal</span>
                <span>Overweight</span>
                <span>Obese</span>
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 2: Gaya Hidup & Riwayat -->
        <div v-show="step === 2" class="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
          <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-10 w-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">2</div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">Gaya Hidup & Penyakit Penyerta</h3>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="md:col-span-1 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Status Merokok</label>
              <div class="space-y-2">
                <label v-for="opt in [{v:'never', l:'Tidak Pernah'}, {v:'former', l:'Mantan Perokok'}, {v:'current', l:'Perokok Aktif'}]" :key="opt.v" class="flex items-center p-3 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" :class="{'border-blue-500 bg-blue-50/50 dark:bg-blue-900/20': formData.smoking_status === opt.v}">
                  <input type="radio" v-model="formData.smoking_status" :value="opt.v" class="w-4 h-4 text-blue-600 accent-blue-600" />
                  <span class="ml-3 font-medium text-slate-700 dark:text-slate-300">{{ opt.l }}</span>
                </label>
              </div>
            </div>

            <div class="md:col-span-1 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Konsumsi Alkohol</label>
              <div class="space-y-2">
                <label v-for="opt in [{v:'none', l:'Tidak Ada'}, {v:'moderate', l:'Sedang'}, {v:'heavy', l:'Berat'}]" :key="opt.v" class="flex items-center p-3 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" :class="{'border-blue-500 bg-blue-50/50 dark:bg-blue-900/20': formData.alcohol_consumption === opt.v}">
                  <input type="radio" v-model="formData.alcohol_consumption" :value="opt.v" class="w-4 h-4 text-blue-600 accent-blue-600" />
                  <span class="ml-3 font-medium text-slate-700 dark:text-slate-300">{{ opt.l }}</span>
                </label>
              </div>
            </div>

            <!-- iOS style switches with Card Look -->
            <div class="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="flex items-center justify-between p-5 border border-slate-200 dark:border-slate-700 rounded-2xl bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-800/80 shadow-sm">
                <div>
                  <p class="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-blue-500"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    Riwayat Keluarga
                  </p>
                  <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mt-1">Ada riwayat hipertensi di keluarga inti?</p>
                </div>
                <label class="relative inline-flex cursor-pointer items-center">
                  <input type="checkbox" v-model="formData.family_history" class="peer sr-only" />
                  <div class="h-7 w-14 rounded-full bg-slate-200 dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:absolute after:left-[3px] after:top-[3px] after:h-5.5 after:w-5.5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:shadow-sm peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <div class="flex items-center justify-between p-5 border border-slate-200 dark:border-slate-700 rounded-2xl bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-800/80 shadow-sm">
                <div>
                  <p class="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-blue-500"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                    Diabetes
                  </p>
                  <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mt-1">Pasien didiagnosis menderita diabetes?</p>
                </div>
                <label class="relative inline-flex cursor-pointer items-center">
                  <input type="checkbox" v-model="formData.diabetes" class="peer sr-only" />
                  <div class="h-7 w-14 rounded-full bg-slate-200 dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:absolute after:left-[3px] after:top-[3px] after:h-5.5 after:w-5.5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:shadow-sm peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 3: Pengukuran Klinis -->
        <div v-show="step === 3" class="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
          <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-10 w-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">3</div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">Pengukuran Klinis (Tensi)</h3>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="md:col-span-1 space-y-3 relative">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Sistolik (mmHg)</label>
              <div class="relative">
                <input type="number" v-model.number="formData.systolic_bp" class="block w-full rounded-xl border-slate-300 dark:border-slate-700 dark:bg-slate-800 dark:text-white py-3.5 px-4 border shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 sm:text-lg font-mono transition-all" :class="{'border-red-500 ring-2 ring-red-500/20 bg-red-50 dark:bg-red-900/10': errors.systolic_bp}" placeholder="120" />
                <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                  <span class="text-slate-400 font-medium">SYS</span>
                </div>
              </div>
              <p v-if="errors.systolic_bp" class="text-xs font-medium text-red-500 mt-1 animate-in slide-in-from-top-1">{{ errors.systolic_bp }}</p>
            </div>
            
            <div class="md:col-span-1 space-y-3 relative">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Diastolik (mmHg)</label>
              <div class="relative">
                <input type="number" v-model.number="formData.diastolic_bp" class="block w-full rounded-xl border-slate-300 dark:border-slate-700 dark:bg-slate-800 dark:text-white py-3.5 px-4 border shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 sm:text-lg font-mono transition-all" :class="{'border-red-500 ring-2 ring-red-500/20 bg-red-50 dark:bg-red-900/10': errors.diastolic_bp}" placeholder="80" />
                <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                  <span class="text-slate-400 font-medium">DIA</span>
                </div>
              </div>
              <p v-if="errors.diastolic_bp" class="text-xs font-medium text-red-500 mt-1 animate-in slide-in-from-top-1">{{ errors.diastolic_bp }}</p>
            </div>
            
            <div class="md:col-span-2 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Tingkat Kolesterol</label>
              <div class="grid grid-cols-3 gap-3">
                <label v-for="opt in [{v:'normal', l:'Normal'}, {v:'borderline', l:'Ambang Batas'}, {v:'high', l:'Tinggi'}]" :key="opt.v" class="relative cursor-pointer">
                  <input type="radio" v-model="formData.cholesterol_level" :value="opt.v" class="peer sr-only" name="cholesterol" />
                  <div class="h-full rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-4 text-center transition-all peer-checked:border-blue-600 peer-checked:bg-blue-50 dark:peer-checked:bg-blue-900/20 peer-checked:text-blue-700 dark:peer-checked:text-blue-400 hover:bg-slate-50 dark:hover:bg-slate-700/50 flex flex-col items-center justify-center gap-2">
                    <span class="font-bold text-sm leading-tight">{{ opt.l }}</span>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="mt-10 pt-6 flex items-center justify-between border-t border-slate-100 dark:border-slate-800">
          <button type="button" @click="prevStep" :disabled="step === 1" class="px-6 py-3 text-sm font-bold text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl shadow-sm hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-0 disabled:pointer-events-none transition-all active:scale-95">
            &larr; Kembali
          </button>
          
          <button v-if="step < 3" type="button" @click="nextStep" class="px-8 py-3 text-sm font-bold text-white bg-blue-600 rounded-xl shadow-lg shadow-blue-500/30 hover:bg-blue-700 hover:shadow-blue-500/50 transition-all active:scale-95 flex items-center gap-2 ml-auto">
            Selanjutnya &rarr;
          </button>
          
          <button v-if="step === 3" type="submit" :disabled="isSubmitting" class="px-8 py-3 text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-blue-600 rounded-xl shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900 disabled:opacity-70 transition-all active:scale-95 flex items-center gap-2 ml-auto">
            <svg v-if="isSubmitting" class="h-5 w-5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            {{ isSubmitting ? 'Menganalisis...' : 'Proses Analisis AI' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { z } from 'zod'
import { screeningService } from '../../services/screeningService'

const router = useRouter()
const route = useRoute()
const step = ref(1)
const isSubmitting = ref(false)
const formErrors = ref(false)

// Data state
const formData = reactive({
  nik: '',
  name: '',
  date_of_birth: '',
  age: 45,
  gender: '',
  bmi: 22.5,
  smoking_status: 'never',
  alcohol_consumption: 'none',
  physical_activity: 'moderate',
  family_history: false,
  diabetes: false,
  systolic_bp: 120,
  diastolic_bp: 80,
  cholesterol_level: 'normal'
})

// Validation State
const errors = reactive<Record<string, string>>({})

// Zod Schemas per step for partial validation
const step1Schema = z.object({
  nik: z.string().length(16, 'NIK harus 16 digit'),
  name: z.string().min(3, 'Nama minimal 3 karakter'),
  date_of_birth: z.string().min(1, 'Tanggal lahir wajib diisi'),
  age: z.number().min(18, 'Minimal usia 18 tahun').max(100),
  gender: z.string().min(1, 'Jenis kelamin wajib dipilih'),
  bmi: z.number().min(10).max(60)
})

const step3Schema = z.object({
  systolic_bp: z.number().min(70, 'Sistolik terlalu rendah').max(250, 'Sistolik terlalu tinggi'),
  diastolic_bp: z.number().min(40, 'Diastolik terlalu rendah').max(150, 'Diastolik terlalu tinggi'),
})

const triggerShake = () => {
  formErrors.value = true
  setTimeout(() => { formErrors.value = false }, 500)
}

const validateStep = (currentStep: number): boolean => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  try {
    if (currentStep === 1) {
      step1Schema.parse(formData)
    } else if (currentStep === 3) {
      step3Schema.parse(formData)
    }
    return true
  } catch (err) {
    if (err instanceof z.ZodError) {
      err.errors.forEach(e => {
        if (e.path[0]) {
          errors[e.path[0] as string] = e.message
        }
      })
    }
    triggerShake()
    return false
  }
}

const nextStep = () => {
  if (validateStep(step.value)) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    step.value++
  }
}

const prevStep = () => {
  if (step.value > 1) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    step.value--
  }
}

const onSubmit = async () => {
  if (!validateStep(3)) return
  
  isSubmitting.value = true
  try {
    const response = await screeningService.createScreening(formData)
    // Success, redirect to XAI dashboard or results
    router.push({ name: 'screening-result', params: { id: response.data.screening_id } })
  } catch (e: any) {
    console.error(e)
    alert(e.response?.data?.message || 'Gagal memproses skrining')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  if (route.query.nik) formData.nik = route.query.nik as string
  if (route.query.name) formData.name = route.query.name as string
  if (route.query.dob) formData.date_of_birth = route.query.dob as string
  if (route.query.gender) formData.gender = route.query.gender as string
})
</script>

<style scoped>
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); }
  60% { transform: translateX(-8px); }
  80% { transform: translateX(8px); }
}
.animate-shake {
  animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}

/* Custom styling for standard range inputs */
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  margin-top: -8px; /* You need to specify a margin in Chrome, but in Firefox and IE it is automatic */
  box-shadow: 0 0 10px rgba(37,99,235,0.3);
  transition: transform 0.1s;
}

input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

input[type=range]::-webkit-slider-runnable-track {
  width: 100%;
  height: 6px;
  cursor: pointer;
  background: #e2e8f0;
  border-radius: 999px;
}

:global(.dark) input[type=range]::-webkit-slider-runnable-track {
  background: #334155;
}
</style>
