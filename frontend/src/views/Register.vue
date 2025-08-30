<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Create Account</h1>
      <p class="subtitle">Join us and start planning your projects!</p>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="Enter your email"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="username">Username (optional)</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter a username"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="password1">Password</label>
          <input
            type="password"
            id="password1"
            v-model="password1"
            required
            placeholder="Enter your password"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="password2">Confirm Password</label>
          <input
            type="password"
            id="password2"
            v-model="password2"
            required
            placeholder="Confirm your password"
            class="form-input"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>
      
      <div class="oauth-section">
        <div class="divider">
          <span>or</span>
        </div>
        
        <div class="oauth-buttons">
          <button @click="handleGoogleOAuth" class="oauth-btn google-btn" :disabled="oauthLoading">
            <svg class="oauth-icon" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            {{ oauthLoading ? 'Signing up...' : 'Sign up with Google' }}
          </button>
        </div>
      </div>
      
      <div class="links">
        <p>
          Already have an account? 
          <router-link to="/login" class="link">Sign in</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const email = ref('')
    const username = ref('')
    const password1 = ref('')
    const password2 = ref('')
    const loading = ref(false)
    const oauthLoading = ref(false)
    const error = ref('')
    
    const handleRegister = async () => {
      loading.value = true
      error.value = ''
      
      // Basic validation
      if (password1.value !== password2.value) {
        error.value = 'Passwords do not match.'
        loading.value = false
        return
      }
      
      const result = await authStore.register(
        email.value, 
        password1.value, 
        password2.value, 
        username.value
      )
      
      if (result.success) {
        router.push('/')
      } else {
        error.value = result.error?.non_field_errors?.[0] || 
                     result.error?.email?.[0] || 
                     result.error?.password1?.[0] || 
                     result.error?.password2?.[0] || 
                     'Registration failed. Please try again.'
      }
      
      loading.value = false
    }
    
    const handleGoogleOAuth = async () => {
      oauthLoading.value = true
      error.value = ''
      
      try {
        const oauthUrl = await authStore.getGoogleOAuthUrl()
        window.location.href = oauthUrl
      } catch (err) {
        error.value = 'Failed to start OAuth process. Please try again.'
        oauthLoading.value = false
      }
    }
    
    return {
      email,
      username,
      password1,
      password2,
      loading,
      oauthLoading,
      error,
      handleRegister,
      handleGoogleOAuth
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.subtitle {
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #2c3e50;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid #e1e8ed;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.btn {
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
}

.links {
  text-align: center;
  margin-top: 1.5rem;
}

.link {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

.oauth-section {
  margin-top: 2rem;
}

.divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e1e8ed;
}

.divider span {
  background: white;
  padding: 0 1rem;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.oauth-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.oauth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 2px solid #e1e8ed;
  border-radius: 6px;
  background: white;
  color: #2c3e50;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.oauth-btn:hover:not(:disabled) {
  border-color: #3498db;
  transform: translateY(-1px);
}

.oauth-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.google-btn {
  border-color: #4285F4;
  color: #4285F4;
}

.google-btn:hover:not(:disabled) {
  background: #4285F4;
  color: white;
}

.oauth-icon {
  width: 20px;
  height: 20px;
}
</style> 