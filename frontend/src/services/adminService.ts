import api from './api'
import type { User } from '../types/auth'

export const adminService = {
  getUsers: async (search?: string) => {
    const params = search ? { search } : {}
    const response = await api.get('/admin/users', { params })
    return response.data
  },

  createUser: async (data: any) => {
    const response = await api.post('/admin/users', data)
    return response.data.data
  },

  updateUser: async (id: number, data: any) => {
    const response = await api.put(`/admin/users/${id}`, data)
    return response.data.data
  },

  deleteUser: async (id: number) => {
    const response = await api.delete(`/admin/users/${id}`)
    return response.data
  },

  getAuditLogs: async (page = 1) => {
    const response = await api.get('/admin/audit-logs', { params: { page } })
    return response.data
  }
}
