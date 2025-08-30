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
    
    return {
      email,
      username,
      password1,
      password2,
      loading,
      error,
      handleRegister
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
</style> 