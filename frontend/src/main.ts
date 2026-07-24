import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import VChart from 'vue-echarts'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/authStore'
import './assets/styles/globals.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(VueQueryPlugin)
app.component('v-chart', VChart)

// Pulihkan sesi dari token yang tersimpan sebelum aplikasi dipasang, supaya
// status login sudah diketahui pada render pertama. Router memakai promise yang
// sama lewat ensureInitialized(), jadi pengecekan hanya terjadi satu kali.
const authStore = useAuthStore()
authStore.ensureInitialized().finally(() => {
  app.mount('#app')
})
