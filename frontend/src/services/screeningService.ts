import api from './api'

// =====================================================================
// Screening Service — satu-satunya sumber hasil skrining adalah backend
// Laravel + ML Engine (XGBoost-SGO).
//
// TIDAK ADA mode offline / prediksi cadangan. Jika backend atau ML Engine
// tidak dapat dihubungi, error diteruskan ke halaman pemanggil supaya
// pengguna melihat pesan kesalahan yang jujur — bukan angka hasil karangan
// yang bisa disalahartikan sebagai keluaran model.
// =====================================================================

export const screeningService = {
  createScreening: async (data: any) => {
    const res = await api.post('/screenings', data)
    return res.data
  },

  getScreening: async (id: number | string) => {
    const res = await api.get(`/screenings/${id}`)
    return res.data
  },

  getScreenings: async (page = 1) => {
    const res = await api.get('/screenings', { params: { page } })
    return res.data
  },
}
