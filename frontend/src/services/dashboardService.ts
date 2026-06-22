import api from './api'

export const dashboardService = {
  getStats: async () => {
    const response = await api.get('/dashboard/stats')
    return response.data.data
  },

  getRiskDistribution: async () => {
    const response = await api.get('/dashboard/risk-distribution')
    return response.data.data
  },

  getFeatureImportance: async () => {
    const response = await api.get('/dashboard/feature-importance')
    return response.data.data
  },
  
  getMonthlyTrend: async () => {
    const response = await api.get('/dashboard/monthly-trend')
    return response.data.data
  }
}
