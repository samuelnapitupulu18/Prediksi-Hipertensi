import api from './api'
import type { Patient } from '../types/patient'

export const patientService = {
  getPatients: async (search?: string) => {
    const params = search ? { search } : {}
    const response = await api.get('/patients', { params })
    return response.data
  },

  getPatient: async (id: number) => {
    const response = await api.get(`/patients/${id}`)
    return response.data.data
  },

  createPatient: async (data: Omit<Patient, 'id' | 'created_at' | 'updated_at'>) => {
    const response = await api.post('/patients', data)
    return response.data.data
  },

  updatePatient: async (id: number, data: Partial<Patient>) => {
    const response = await api.put(`/patients/${id}`, data)
    return response.data.data
  },

  deletePatient: async (id: number) => {
    const response = await api.delete(`/patients/${id}`)
    return response.data
  }
}
