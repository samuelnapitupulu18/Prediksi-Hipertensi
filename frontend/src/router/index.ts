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
          meta: { roles: ['dokter', 'perawat'] }
        },
        {
          path: 'screening/history',
          name: 'screening-history',
          component: () => import('../pages/screening/ScreeningHistory.vue'),
          meta: { roles: ['super_admin', 'dokter', 'perawat'] }
        },
        {
          path: 'screening/:id',
          name: 'screening-result',
          component: () => import('../pages/screening/ScreeningResult.vue'),
          meta: { roles: ['super_admin', 'dokter', 'perawat'] }
        },
        {
          path: 'xai',
          name: 'xai-dashboard',
          component: () => import('../pages/xai/XAIDashboard.vue'),
          meta: { roles: ['super_admin', 'dokter'] }
        },
        {
          path: 'admin/users',
          name: 'admin-users',
          component: () => import('../pages/admin/UserManagement.vue'),
          meta: { roles: ['super_admin'] }
        },
        {
          path: 'patients',
          name: 'patient-list',
          component: () => import('../pages/patients/PatientList.vue'),
          meta: { roles: ['super_admin', 'dokter', 'perawat'] }
        },
        {
          path: 'patients/:id',
          name: 'patient-detail',
          component: () => import('../pages/patients/PatientDetail.vue'),
          meta: { roles: ['super_admin', 'dokter', 'perawat'] }
        }
      ]
    }
  ]
})

// Navigation Guards
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } else if (to.meta.roles && authStore.user) {
    // Role based access control
    const allowedRoles = to.meta.roles as string[]
    if (!allowedRoles.includes(authStore.user.role)) {
      // Could redirect to a 403 page instead
      next({ name: 'dashboard' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
