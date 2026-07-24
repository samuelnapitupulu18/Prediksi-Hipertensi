import axios from 'axios'

const api = axios.create({
  // Pointing to the Nginx reverse proxy
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  // Use stateless bearer tokens instead of cookies
  withCredentials: false,
  withXSRFToken: false,
})

// Load bearer token from localStorage on startup
const savedToken = localStorage.getItem('auth_token')
if (savedToken) {
  api.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`
}

// Add response interceptor for global error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token tidak berlaku lagi → bersihkan sesi
      localStorage.removeItem('auth_token')
      delete api.defaults.headers.common['Authorization']
    }
    return Promise.reject(error)
  }
)

export default api
