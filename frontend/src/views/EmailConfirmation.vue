<template>
  <div class="email-confirmation">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-12 col-sm-8 col-md-6 col-lg-4">
        <div class="card shadow-lg border-0">
          <div class="card-body p-4 p-md-5 text-center">
            <div class="mb-4">
              <i class="bi bi-envelope-check text-success" style="font-size: 3rem;"></i>
            </div>
            
            <h1 class="h3 text-dark mb-3">Email Verification</h1>
            
            <div v-if="loading" class="mb-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="text-muted mt-2">Verifying your email...</p>
            </div>
            
            <div v-else-if="success" class="mb-4">
              <div class="alert alert-success" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                Your email has been successfully verified!
              </div>
              <p class="text-muted">You can now log in to your account.</p>
              <router-link to="/login" class="btn btn-primary">
                <i class="bi bi-box-arrow-in-right me-2"></i>Go to Login
              </router-link>
            </div>
            
            <div v-else-if="error" class="mb-4">
              <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>
              <p class="text-muted">Please try again or contact support if the problem persists.</p>
              <router-link to="/register" class="btn btn-outline-primary">
                <i class="bi bi-arrow-left me-2"></i>Back to Register
              </router-link>
            </div>
            
            <div v-else class="mb-4">
              <p class="text-muted">Please check your email and click the verification link to activate your account.</p>
              <p class="text-muted small">Didn't receive the email? Check your spam folder or try registering again.</p>
              <router-link to="/register" class="btn btn-outline-primary">
                <i class="bi bi-arrow-left me-2"></i>Back to Register
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'EmailConfirmation',
  setup() {
    const route = useRoute()
    const loading = ref(false)
    const success = ref(false)
    const error = ref('')
    
    const verifyEmail = async () => {
      const key = route.query.key
      
      if (!key) {
        error.value = 'Invalid verification link. Please check your email for the correct link.'
        return
      }
      
      loading.value = true
      
      try {
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await axios.post(`${API_URL}/api/auth/registration/verify-email/`, {
          key: key
        })
        
        success.value = true
      } catch (err) {
        console.error('Email verification error:', err)
        error.value = err.response?.data?.detail || 'Email verification failed. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      verifyEmail()
    })
    
    return {
      loading,
      success,
      error
    }
  }
}
</script>

<style scoped>
.email-confirmation {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 1rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.2) !important;
}

@media (max-width: 767.98px) {
  .card {
    margin: 1rem;
  }
  
  .card-body {
    padding: 2rem !important;
  }
}
</style> 