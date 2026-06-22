<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-slate-800 dark:text-white">Daftar Pasien</h1>
      <div class="flex items-center gap-2">
        <button @click="openAddModal" class="bg-white border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:bg-slate-900 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          + Tambah Pasien
        </button>
        <router-link :to="{ name: 'screening-new' }" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          + Skrining Baru
        </router-link>
      </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
      <div class="p-4 border-b border-slate-200 dark:border-slate-700">
        <input 
          v-model="search" 
          @input="fetchPatients"
          type="text" 
          placeholder="Cari nama atau NIK..." 
          class="w-full md:w-1/3 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
        />
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-600 dark:text-slate-300">
          <thead class="bg-slate-50 dark:bg-slate-900/50 text-slate-500 dark:text-slate-400 font-medium border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="px-6 py-4">NIK</th>
              <th class="px-6 py-4">Nama Pasien</th>
              <th class="px-6 py-4">Usia / Gender</th>
              <th class="px-6 py-4">Tanggal Lahir</th>
              <th class="px-6 py-4 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="animate-pulse">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">Memuat data...</td>
            </tr>
            <tr v-else-if="patients.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">Tidak ada pasien ditemukan.</td>
            </tr>
            <tr v-for="patient in patients" :key="patient.id" class="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
              <td class="px-6 py-4 font-mono text-xs">{{ patient.nik }}</td>
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">{{ patient.name }}</td>
              <td class="px-6 py-4">
                {{ calculateAge(patient.date_of_birth) }} th / 
                {{ patient.gender === 'male' ? 'L' : 'P' }}
              </td>
              <td class="px-6 py-4">{{ patient.date_of_birth }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <router-link :to="{ name: 'patient-detail', params: { id: patient.id } }" class="text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium" title="Detail & Riwayat">
                    Detail
                  </router-link>
                  <button @click="openEditModal(patient)" class="text-amber-600 dark:text-amber-400 hover:underline text-sm font-medium" title="Edit Data">
                    Edit
                  </button>
                  <button @click="deletePatientData(patient.id)" class="text-red-600 dark:text-red-400 hover:underline text-sm font-medium" title="Hapus Data">
                    Hapus
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Form -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
      <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="p-6 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center">
          <h3 class="text-lg font-bold text-slate-900 dark:text-white">{{ isEditing ? 'Edit Data Pasien' : 'Tambah Pasien Baru' }}</h3>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-500">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          </button>
        </div>
        <form @submit.prevent="submitForm" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">NIK (16 Digit)</label>
            <input v-model="formData.nik" type="text" required pattern="[0-9]{16}" class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Nama Lengkap</label>
            <input v-model="formData.name" type="text" required class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Tanggal Lahir</label>
              <input v-model="formData.date_of_birth" type="date" required class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Jenis Kelamin</label>
              <select v-model="formData.gender" required class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none">
                <option value="male">Laki-laki</option>
                <option value="female">Perempuan</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">No. HP (Opsional)</label>
            <input v-model="formData.phone" type="text" class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Alamat (Opsional)</label>
            <textarea v-model="formData.address" rows="2" class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"></textarea>
          </div>
          
          <div class="pt-4 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors">Batal</button>
            <button type="submit" :disabled="saving" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50">
              {{ saving ? 'Menyimpan...' : 'Simpan Data' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { patientService } from '../../services/patientService'

const patients = ref<any[]>([])
const loading = ref(true)
const search = ref('')

const showModal = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const formData = ref({
  id: 0,
  nik: '',
  name: '',
  date_of_birth: '',
  gender: 'male',
  phone: '',
  address: ''
})

const fetchPatients = async () => {
  loading.value = true
  try {
    const data = await patientService.getPatients(search.value)
    patients.value = data.data // pagination data array
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

const openAddModal = () => {
  isEditing.value = false
  formData.value = { id: 0, nik: '', name: '', date_of_birth: '', gender: 'male', phone: '', address: '' }
  showModal.value = true
}

const openEditModal = (patient: any) => {
  isEditing.value = true
  formData.value = {
    id: patient.id,
    nik: patient.nik,
    name: patient.name,
    date_of_birth: patient.date_of_birth,
    gender: patient.gender,
    phone: patient.phone || '',
    address: patient.address || ''
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitForm = async () => {
  saving.value = true
  try {
    if (isEditing.value) {
      await patientService.updatePatient(formData.value.id, formData.value)
      alert('Data pasien berhasil diperbarui!')
    } else {
      await patientService.createPatient(formData.value)
      alert('Pasien baru berhasil didaftarkan!')
    }
    closeModal()
    fetchPatients()
  } catch (e: any) {
    alert('Terjadi kesalahan: ' + (e.response?.data?.message || e.message))
    console.error(e)
  } finally {
    saving.value = false
  }
}

const deletePatientData = async (id: number) => {
  if (confirm('Apakah Anda yakin ingin menghapus data pasien ini? Seluruh riwayat skriningnya juga akan terhapus.')) {
    try {
      await patientService.deletePatient(id)
      alert('Data pasien berhasil dihapus.')
      fetchPatients()
    } catch (e: any) {
      alert('Terjadi kesalahan saat menghapus data.')
      console.error(e)
    }
  }
}

onMounted(() => {
  fetchPatients()
})
</script>
