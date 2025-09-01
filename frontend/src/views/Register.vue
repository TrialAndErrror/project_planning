<template>
  <div class="register-container">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-12 col-sm-8 col-md-6 col-lg-4">
        <div class="card shadow-lg border-0 register-card">
          <div class="card-body p-4 p-md-5">
            <div class="text-center mb-4">
              <h1 class="h2 text-dark mb-2">Create Account</h1>
              <p class="text-muted mb-0">Join us and start planning your projects!</p>
            </div>
            
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  required
                  placeholder="Enter your email"
                  class="form-control"
                />
              </div>
              
              <div class="mb-3">
                <label for="username" class="form-label">Username <span class="text-muted">(optional)</span></label>
                <input
                  type="text"
                  id="username"
                  v-model="username"
                  placeholder="Enter a username"
                  class="form-control"
                />
              </div>
              
              <div class="mb-3">
                <label for="password1" class="form-label">Password</label>
                <input
                  type="password"
                  id="password1"
                  v-model="password1"
                  required
                  placeholder="Enter your password"
                  class="form-control"
                />
              </div>
              
              <div class="mb-4">
                <label for="password2" class="form-label">Confirm Password</label>
                <input
                  type="password"
                  id="password2"
                  v-model="password2"
                  required
                  placeholder="Confirm your password"
                  class="form-control"
                />
              </div>
              
              <div v-if="error" class="alert alert-danger mb-4" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>
              
              <div v-if="success" class="alert alert-success mb-4" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                {{ success }}
              </div>
              
              <button type="submit" class="btn btn-primary w-100 mb-3" :disabled="loading">
                <span v-if="loading" class="d-flex align-items-center justify-content-center">
                  <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  Creating account...
                </span>
                <span v-else>
                  <i class="bi bi-person-plus me-2"></i>Create Account
                </span>
              </button>
            </form>
            
            <div class="text-center">
              <p class="text-muted mb-0">
                Already have an account? 
                <router-link to="/login" class="text-decoration-none fw-semibold">Sign in</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const password1 = ref('')
const password2 = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
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
    success.value = result.message || 'Registration successful! Please check your email to verify your account.'
    // Clear form
    email.value = ''
    username.value = ''
    password1.value = ''
    password2.value = ''
  } else {
    error.value = result.error?.non_field_errors?.[0] || 
                 result.error?.email?.[0] || 
                 result.error?.password1?.[0] || 
                 result.error?.password2?.[0] || 
                 'Registration failed. Please try again.'
  }
  
  loading.value = false
}
</script>

<style scoped>
.register-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.register-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 1rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.register-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.2) !important;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #0b5ed7 0%, #0a58ca 100%);
  transform: translateY(-1px);
  box-shadow: 0 0.5rem 1rem rgba(13, 110, 253, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  transform: none;
}

@media (max-width: 767.98px) {
  .register-card {
    margin: 1rem;
  }
  
  .card-body {
    padding: 2rem !important;
  }
}
</style> 