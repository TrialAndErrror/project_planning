import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(false)

  // Configure axios defaults
  axios.defaults.baseURL = API_URL
  axios.defaults.withCredentials = true

  // Set auth token in axios headers
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
  }

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/auth/login/', {
        email,
        password
      })
      
      const { key, user: userData } = response.data
      
      token.value = key
      user.value = userData
      isAuthenticated.value = true
      
      localStorage.setItem('token', key)
      axios.defaults.headers.common['Authorization'] = `Token ${key}`
      
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.response?.data || 'Login failed' 
      }
    }
  }

  const register = async (email, password1, password2, username = '') => {
    try {
      const response = await axios.post('/api/auth/registration/', {
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
      axios.defaults.headers.common['Authorization'] = `Token ${key}`
      
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
      await axios.post('/api/auth/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local state regardless of API call success
      token.value = null
      user.value = null
      isAuthenticated.value = false
      
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }

  const checkAuth = async () => {
    if (!token.value) {
      isAuthenticated.value = false
      return
    }

    try {
      const response = await axios.get('/api/users/auth-status/')
      if (response.data.authenticated) {
        user.value = response.data.user
        isAuthenticated.value = true
      } else {
        // Token is invalid, clear it
        token.value = null
        user.value = null
        isAuthenticated.value = false
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      }
    } catch (error) {
      console.error('Auth check error:', error)
      // Clear invalid token
      token.value = null
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }

  const getOAuthProviders = async () => {
    try {
      const response = await axios.get('/api/users/oauth/providers/')
      return response.data.providers
    } catch (error) {
      console.error('Failed to get OAuth providers:', error)
      return []
    }
  }

  const getGoogleOAuthUrl = async () => {
    try {
      const response = await axios.get('/api/users/oauth/google/url/')
      return response.data.oauth_url
    } catch (error) {
      console.error('Failed to get Google OAuth URL:', error)
      throw error
    }
  }

  const handleOAuthCallback = async (code) => {
    try {
      const response = await axios.post('/api/users/oauth/google/callback/', {
        code: code
      })
      
      const { token: authToken, user: userData } = response.data
      
      token.value = authToken
      user.value = userData
      isAuthenticated.value = true
      
      localStorage.setItem('token', authToken)
      axios.defaults.headers.common['Authorization'] = `Token ${authToken}`
      
      return { success: true, isNewUser: response.data.is_new_user }
    } catch (error) {
      console.error('OAuth callback error:', error)
      return { 
        success: false, 
        error: error.response?.data || 'OAuth authentication failed' 
      }
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth,
    getOAuthProviders,
    getGoogleOAuthUrl,
    handleOAuthCallback
  }
}) 