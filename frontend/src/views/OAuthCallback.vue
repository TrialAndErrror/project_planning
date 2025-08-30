<template>
  <div class="oauth-callback">
    <div class="callback-card">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <h2>Authenticating...</h2>
        <p>Please wait while we complete your sign-in.</p>
      </div>
      
      <div v-else-if="error" class="error">
        <h2>Authentication Failed</h2>
        <p>{{ error }}</p>
        <button @click="goToLogin" class="btn btn-primary">Back to Login</button>
      </div>
      
      <div v-else-if="success" class="success">
        <h2>Welcome{{ isNewUser ? '!' : ' back!' }}</h2>
        <p>{{ isNewUser ? 'Your account has been created successfully.' : 'You have been signed in successfully.' }}</p>
        <button @click="goToHome" class="btn btn-primary">Continue to Dashboard</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'OAuthCallback',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    const loading = ref(true)
    const error = ref('')
    const success = ref(false)
    const isNewUser = ref(false)
    
    const handleCallback = async () => {
      try {
        const code = route.query.code
        if (!code) {
          error.value = 'No authorization code provided.'
          loading.value = false
          return
        }
        
        const result = await authStore.handleOAuthCallback(code)
        
        if (result.success) {
          success.value = true
          isNewUser.value = result.isNewUser
        } else {
          error.value = result.error || 'Authentication failed.'
        }
      } catch (err) {
        error.value = 'An unexpected error occurred.'
        console.error('OAuth callback error:', err)
      } finally {
        loading.value = false
      }
    }
    
    const goToLogin = () => {
      router.push('/login')
    }
    
    const goToHome = () => {
      router.push('/')
    }
    
    onMounted(() => {
      handleCallback()
    })
    
    return {
      loading,
      error,
      success,
      isNewUser,
      goToLogin,
      goToHome
    }
  }
}
</script>

<style scoped>
.oauth-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.callback-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

.loading h2,
.error h2,
.success h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.loading p,
.error p,
.success p {
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  color: #e74c3c;
}

.success {
  color: #27ae60;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-1px);
}
</style> 