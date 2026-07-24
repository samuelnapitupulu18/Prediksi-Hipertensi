import api from './api'

// =====================================================================
// Dashboard Service — seluruh statistik dihitung backend Laravel dari
// isi database. Tidak ada perhitungan cadangan di sisi browser, sehingga
// angka yang tampil selalu dapat ditelusuri ke tabel screenings/predictions.
// =====================================================================

export const dashboardService = {
  getStats: async () => {
    const res = await api.get('/dashboard/stats')
    return res.data.data
  },

  getRiskDistribution: async () => {
    const res = await api.get('/dashboard/risk-distribution')
    return res.data.data
  },

  getFeatureImportance: async () => {
    const res = await api.get('/dashboard/feature-importance')
    return res.data.data
  },

  getMonthlyTrend: async () => {
    const res = await api.get('/dashboard/monthly-trend')
    return res.data.data
  },
}
