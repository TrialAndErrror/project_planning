<template>
  <div class="home">
    <div class="welcome-card">
      <h1>Welcome to Project Planning!</h1>
      <p class="subtitle">Your project management solution</p>
      
      <div class="user-info" v-if="authStore.user">
        <h2>Hello, {{ authStore.user.email }}!</h2>
        <p>You are successfully logged in.</p>
      </div>
      
      <div class="features">
        <h3>What you can do:</h3>
        <ul>
          <li>Create and manage projects</li>
          <li>Track tasks and milestones</li>
          <li>Collaborate with team members</li>
          <li>Monitor progress and deadlines</li>
        </ul>
      </div>
      
      <div class="actions">
        <button class="btn btn-primary">Create New Project</button>
        <button class="btn btn-secondary">View Projects</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    
    return {
      authStore
    }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
}

.welcome-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 600px;
  width: 100%;
}

h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.user-info {
  background: #ecf0f1;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.user-info h2 {
  color: #27ae60;
  margin-bottom: 0.5rem;
}

.features {
  text-align: left;
  margin: 2rem 0;
}

.features h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.features ul {
  list-style: none;
  padding: 0;
}

.features li {
  padding: 0.5rem 0;
  color: #34495e;
  position: relative;
  padding-left: 1.5rem;
}

.features li::before {
  content: "✓";
  color: #27ae60;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}
</style> 