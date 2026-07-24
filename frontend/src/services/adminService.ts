import api from './api'

// =====================================================================
// Admin Service — rute /admin pada backend Laravel, dijaga middleware
// `role:super_admin`.
//
// Konsisten dengan layanan lain: tidak ada data cadangan maupun daftar
// kosong palsu. Kegagalan diteruskan sebagai error agar halaman dapat
// menampilkan pesan yang jujur, bukan tabel kosong yang menyesatkan.
// =====================================================================

export const adminService = {
  getUsers: async (search?: string, role?: string) => {
    const res = await api.get('/admin/users', { params: { search, role } })
    return res.data
  },

  createUser: async (data: any) => {
    const res = await api.post('/admin/users', data)
    return res.data
  },

  updateUser: async (id: number, data: any) => {
    const res = await api.put(`/admin/users/${id}`, data)
    return res.data
  },

  deleteUser: async (id: number) => {
    const res = await api.delete(`/admin/users/${id}`)
    return res.data
  },

  getAuditLogs: async (page = 1) => {
    const res = await api.get('/admin/audit-logs', { params: { page } })
    return res.data
  },
}
