import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../pages/auth/LoginPage.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/',
      component: () => import('../layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/dashboard'
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('../pages/dashboard/DashboardPage.vue'),
        },
        {
          path: 'screening/new',
          name: 'screening-new',
          component: () => import('../pages/screening/ScreeningForm.vue'),
        },
        {
          path: 'screening/history',
          name: 'screening-history',
          component: () => import('../pages/screening/ScreeningHistory.vue'),
        },
        {
          path: 'screening/:id',
          name: 'screening-result',
          component: () => import('../pages/screening/ScreeningResult.vue'),
        },
        {
          path: 'xai',
          name: 'xai-dashboard',
          component: () => import('../pages/xai/XAIDashboard.vue'),
        },
        {
          path: 'model-accuracy',
          name: 'model-accuracy',
          component: () => import('../pages/xai/ModelAccuracyComparison.vue'),
        },
        {
          path: 'live-comparison',
          name: 'live-comparison',
          component: () => import('../pages/xai/LivePredictionComparison.vue'),
        },
        {
          path: 'patients',
          name: 'patient-list',
          component: () => import('../pages/patients/PatientList.vue'),
        },
        {
          path: 'patients/:id',
          name: 'patient-detail',
          component: () => import('../pages/patients/PatientDetail.vue'),
        },
        // Halaman khusus super admin — dijaga oleh navigation guard di bawah
        // dan oleh middleware `role:super_admin` pada backend.
        {
          path: 'admin/users',
          name: 'admin-users',
          component: () => import('../pages/admin/UserManagement.vue'),
          meta: { requiresSuperAdmin: true },
        },
        {
          path: 'admin/audit-logs',
          name: 'admin-audit-logs',
          component: () => import('../pages/admin/AuditLog.vue'),
          meta: { requiresSuperAdmin: true },
        }
      ]
    }
  ]
})

// Navigation Guards
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  // Tunggu pengecekan token selesai sebelum memutuskan. Wajib, karena navigasi
  // pertama dijalankan saat router dipasang — sebelum sesi sempat dipulihkan.
  await authStore.ensureInitialized()


  // Check the deepest matched route's own requiresAuth meta
  // Child routes can override parent's requiresAuth with their own meta
  const requiresAuth = to.matched.length > 0
    ? to.matched[to.matched.length - 1].meta.requiresAuth !== false && to.matched.some(r => r.meta.requiresAuth === true)
    : false

  const requiresSuperAdmin = to.matched.some((r) => r.meta.requiresSuperAdmin === true)

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (requiresSuperAdmin && !authStore.isSuperAdmin) {
    // Bukan super admin — kembalikan ke dasbor daripada menampilkan halaman
    // yang permintaannya pasti ditolak backend.
    next({ name: 'dashboard' })
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
