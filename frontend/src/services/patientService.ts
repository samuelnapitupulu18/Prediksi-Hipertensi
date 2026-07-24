import api from './api'

// =====================================================================
// Patient Service — seluruh data pasien berasal dari backend Laravel.
// Tidak ada data cadangan lokal; kegagalan jaringan diteruskan sebagai
// error agar tidak ada data fiktif yang tampil di layar.
// =====================================================================

export const patientService = {
  getPatients: async (search?: string) => {
    const res = await api.get('/patients', { params: search ? { search } : {} })
    return res.data
  },

  getPatient: async (id: number | string) => {
    const res = await api.get(`/patients/${id}`)
    // Controller membungkus respons dalam { data: patient }
    return res.data.data ?? res.data
  },

  createPatient: async (data: any) => {
    const res = await api.post('/patients', data)
    return res.data
  },

  updatePatient: async (id: number, data: any) => {
    const res = await api.put(`/patients/${id}`, data)
    return res.data
  },

  deletePatient: async (id: number) => {
    const res = await api.delete(`/patients/${id}`)
    return res.data
  },
}
