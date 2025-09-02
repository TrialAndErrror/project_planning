<template>
  <div class="login-page" :class="{ 'login-shake': loading, 'login-success': loginSuccess }">
    <!-- Background that will transform into navbar -->
    <div class="login-background" :class="{ 'background-pull-up': loginSuccess }"></div>
    
    <!-- Login Form Container -->
    <div class="login-form-container" :class="{ 'form-fade-out': loginSuccess }">
      <div class="login-form-wrapper">
        <div class="login-form-card">
          <div class="login-header">
            <div class="logo-container">
              <i class="bi bi-kanban logo-icon"></i>
            </div>
            <h1 class="login-title">Welcome Back</h1>
            <p class="login-subtitle">Sign in to continue to your projects</p>
          </div>
          
          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label for="email" class="form-label">
                <i class="bi bi-envelope me-2"></i>Email Address
              </label>
              <input
                type="email"
                id="email"
                v-model="email"
                required
                placeholder="Enter your email"
                class="form-control"
                :disabled="loading"
              />
            </div>
            
            <div class="form-group">
              <label for="password" class="form-label">
                <i class="bi bi-lock me-2"></i>Password
              </label>
              <input
                type="password"
                id="password"
                v-model="password"
                required
                placeholder="Enter your password"
                class="form-control"
                :disabled="loading"
              />
            </div>
            
            <div v-if="error" class="error-message" :class="{ 'error-shake': error }">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ error }}
            </div>
            
            <button type="submit" class="login-button" :disabled="loading">
              <span v-if="loading" class="button-content">
                <div class="spinner"></div>
                <span>Signing in...</span>
              </span>
              <span v-else class="button-content">
                <i class="bi bi-box-arrow-in-right me-2"></i>
                Sign In
              </span>
            </button>
          </form>
          
          <div class="login-footer">
            <p class="signup-text">
              Don't have an account? 
              <router-link to="/register" class="signup-link">Sign up</router-link>
            </p>
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
const password = ref('')
const loading = ref(false)
const error = ref('')
const loginSuccess = ref(false)

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  const result = await authStore.login(email.value, password.value)
  
  if (result.success) {
    loginSuccess.value = true
    // Wait for animation to complete before redirecting
    setTimeout(() => {
      router.push('/')
    }, 1500)
  } else {
    error.value = result.error?.non_field_errors?.[0] || 
                 result.error?.email?.[0] || 
                 result.error?.password?.[0] || 
                 'Login failed. Please try again.'
  }
  
  loading.value = false
}
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: #2c3e50;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Background that transforms into navbar */
.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #2c3e50;
  z-index: 1;
  transition: transform 1.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.background-pull-up {
  transform: translateY(-4rem); /* Stop at navbar height */
}

/* Login Form Container */
.login-form-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.form-fade-out {
  opacity: 0;
  transform: translateY(-20px);
}

.login-form-wrapper {
  width: 100%;
}

.login-form-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.login-form-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

/* Header */
.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-container {
  margin-bottom: 1rem;
}

.logo-icon {
  font-size: 3rem;
  color: #2c3e50;
  background: linear-gradient(135deg, #3498db, #2c3e50);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #7f8c8d;
  font-size: 1rem;
  margin: 0;
}

/* Form */
.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #ecf0f1;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  background: rgba(255, 255, 255, 1);
}

.form-control:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Error Message */
.error-message {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  border: 1px solid rgba(231, 76, 60, 0.2);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.error-shake {
  animation: errorShake 0.5s ease-in-out;
}

/* Login Button */
.login-button {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #3498db, #2c3e50);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3);
}

.login-button:disabled {
  opacity: 0.8;
  cursor: not-allowed;
  transform: none;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

/* Spinner */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Footer */
.login-footer {
  text-align: center;
}

.signup-text {
  color: #7f8c8d;
  margin: 0;
  font-size: 0.9rem;
}

.signup-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.signup-link:hover {
  color: #2c3e50;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes errorShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Shake animation during login */
.login-shake {
  animation: loginShake 0.5s ease-in-out;
}

@keyframes loginShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

/* Responsive Design */
@media (max-width: 480px) {
  .login-form-container {
    padding: 1rem;
  }
  
  .login-form-card {
    padding: 2rem;
  }
  
  .login-title {
    font-size: 1.75rem;
  }
  
  .logo-icon {
    font-size: 2.5rem;
  }
}

/* Smooth transitions for all interactive elements */
* {
  transition: all 0.3s ease;
}

/* Focus states for accessibility */
.form-control:focus,
.login-button:focus {
  outline: 2px solid #3498db;
  outline-offset: 2px;
}

/* Loading state enhancements */
.login-button:disabled .button-content {
  opacity: 0.8;
}

/* Backdrop blur fallback */
@supports not (backdrop-filter: blur(10px)) {
  .login-form-card {
    background: rgba(255, 255, 255, 0.98);
  }
}
</style> 