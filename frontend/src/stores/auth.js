import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create a local axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(false)

  // Set auth token in axios headers
  if (token.value) {
    api.defaults.headers.common['Authorization'] = `Token ${token.value}`
  }

  const login = async (email, password) => {
    try {
      console.log('Attempting login with:', { email, password: '***' })
      console.log('API URL:', API_URL)
      
      const response = await api.post('/api/auth/login/', {
        email,
        password
      })
      
      console.log('Login response:', response.data)
      
      const { key, user: userData } = response.data
      
      token.value = key
      user.value = userData
      isAuthenticated.value = true
      
      localStorage.setItem('token', key)
      api.defaults.headers.common['Authorization'] = `Token ${key}`
      
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      console.error('Error response:', error.response)
      return { 
        success: false, 
        error: error.response?.data || 'Login failed' 
      }
    }
  }

  const register = async (email, password1, password2, username = '') => {
    try {
      const response = await api.post('/api/auth/registration/', {
        email,
        password1,
        password2,
        username
      })
      
      const { key, user: userData } = response.data
      
      token.value = key
      user.value = userData
      isAuthenticated.value = true
      
      localStorage.setItem('token', key)
      api.defaults.headers.common['Authorization'] = `Token ${key}`
      
      return { success: true }
    } catch (error) {
      console.error('Registration error:', error)
      return { 
        success: false, 
        error: error.response?.data || 'Registration failed' 
      }
    }
  }

  const logout = async () => {
    try {
      await api.post('/api/auth/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local state regardless of API call success
      token.value = null
      user.value = null
      isAuthenticated.value = false
      
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  }

  const checkAuth = async () => {
    if (!token.value) {
      isAuthenticated.value = false
      return
    }

    try {
      const response = await api.get('/api/users/auth-status/')
      if (response.data.authenticated) {
        user.value = response.data.user
        isAuthenticated.value = true
      } else {
        // Token is invalid, clear it
        token.value = null
        user.value = null
        isAuthenticated.value = false
        localStorage.removeItem('token')
        delete api.defaults.headers.common['Authorization']
      }
    } catch (error) {
      console.error('Auth check error:', error)
      // Clear invalid token
      token.value = null
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth
  }
}) 