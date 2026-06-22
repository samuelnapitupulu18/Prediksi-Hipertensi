import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/authStore'
import './assets/styles/globals.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(VueQueryPlugin)

// Attempt to fetch user before mounting the app
// This ensures that we know the auth state on first load
const authStore = useAuthStore()
authStore.fetchUser().finally(() => {
  app.mount('#app')
})
