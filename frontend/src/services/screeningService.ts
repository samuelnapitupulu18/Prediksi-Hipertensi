import api from './api'

export const screeningService = {
  createScreening: async (data: any) => {
    const response = await api.post('/screenings', data)
    return response.data
  },

  getScreening: async (id: number) => {
    const response = await api.get(`/screenings/${id}`)
    return response.data
  },

  getScreenings: async (page = 1) => {
    const response = await api.get('/screenings', { params: { page } })
    return response.data
  }
}
