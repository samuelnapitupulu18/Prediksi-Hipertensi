import axios from 'axios'

const api = axios.create({
  // Pointing to the Nginx reverse proxy
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  // Crucial for Laravel Sanctum authentication (sends cookies)
  withCredentials: true,
  withXSRFToken: true,
})

// Add response interceptor for global error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Logic to clear auth store and redirect to login
      // will be handled in the router or store
    }
    return Promise.reject(error)
  }
)

export default api
