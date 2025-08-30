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

export const useProjectStore = defineStore('project', () => {
  const projects = ref([])
  const currentProject = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Set auth token in axios headers dynamically
  const setAuthToken = () => {
    const token = localStorage.getItem('token')
    if (token) {
      api.defaults.headers.common['Authorization'] = `Token ${token}`
    } else {
      delete api.defaults.headers.common['Authorization']
    }
  }

  // Get all projects
  const fetchProjects = async () => {
    loading.value = true
    error.value = null
    
    try {
      setAuthToken()
      const response = await api.get('/api/projects/')
      projects.value = response.data
      return { success: true, projects: response.data }
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch projects'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Get single project
  const fetchProject = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      setAuthToken()
      const response = await api.get(`/api/projects/${id}/`)
      currentProject.value = response.data
      return { success: true, project: response.data }
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Create project
  const createProject = async (projectData) => {
    loading.value = true
    error.value = null
    
    try {
      setAuthToken()
      const response = await api.post('/api/projects/', projectData)
      const newProject = response.data
      projects.value.unshift(newProject)
      return { success: true, project: newProject }
    } catch (err) {
      error.value = err.response?.data || 'Failed to create project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Update project
  const updateProject = async (id, projectData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.put(`/api/projects/${id}/`, projectData)
      const updatedProject = response.data
      
      // Update in projects list
      const index = projects.value.findIndex(p => p.id === id)
      if (index !== -1) {
        projects.value[index] = updatedProject
      }
      
      // Update current project if it's the one being updated
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = updatedProject
      }
      
      return { success: true, project: updatedProject }
    } catch (err) {
      error.value = err.response?.data || 'Failed to update project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Delete project
  const deleteProject = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/api/projects/${id}/`)
      
      // Remove from projects list
      projects.value = projects.value.filter(p => p.id !== id)
      
      // Clear current project if it's the one being deleted
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = null
      }
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data || 'Failed to delete project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Create stage
  const createStage = async (stageData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/api/stages/', stageData)
      const newStage = response.data
      
      // Add to current project if it exists
      if (currentProject.value && currentProject.value.id === stageData.project) {
        currentProject.value.stages.push(newStage)
      }
      
      return { success: true, stage: newStage }
    } catch (err) {
      error.value = err.response?.data || 'Failed to create stage'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Update stage
  const updateStage = async (id, stageData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.put(`/api/stages/${id}/`, stageData)
      const updatedStage = response.data
      
      // Update in current project
      if (currentProject.value) {
        const stageIndex = currentProject.value.stages.findIndex(s => s.id === id)
        if (stageIndex !== -1) {
          currentProject.value.stages[stageIndex] = updatedStage
        }
      }
      
      return { success: true, stage: updatedStage }
    } catch (err) {
      error.value = err.response?.data || 'Failed to update stage'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Delete stage
  const deleteStage = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/api/stages/${id}/`)
      
      // Remove from current project
      if (currentProject.value) {
        currentProject.value.stages = currentProject.value.stages.filter(s => s.id !== id)
      }
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data || 'Failed to delete stage'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Create task
  const createTask = async (taskData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/api/tasks/', taskData)
      const newTask = response.data
      
      // Add to current project
      if (currentProject.value && currentProject.value.id === taskData.project) {
        currentProject.value.tasks.push(newTask)
      }
      
      return { success: true, task: newTask }
    } catch (err) {
      error.value = err.response?.data || 'Failed to create task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Update task
  const updateTask = async (id, taskData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.put(`/api/tasks/${id}/`, taskData)
      const updatedTask = response.data
      
      // Update in current project
      if (currentProject.value) {
        const taskIndex = currentProject.value.tasks.findIndex(t => t.id === id)
        if (taskIndex !== -1) {
          currentProject.value.tasks[taskIndex] = updatedTask
        }
      }
      
      return { success: true, task: updatedTask }
    } catch (err) {
      error.value = err.response?.data || 'Failed to update task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Delete task
  const deleteTask = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/api/tasks/${id}/`)
      
      // Remove from current project
      if (currentProject.value) {
        currentProject.value.tasks = currentProject.value.tasks.filter(t => t.id !== id)
      }
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data || 'Failed to delete task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Start task
  const startTask = async (id) => {
    try {
      const response = await api.post(`/api/tasks/${id}/start/`)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data || 'Failed to start task' }
    }
  }

  // Complete task
  const completeTask = async (id) => {
    try {
      const response = await api.post(`/api/tasks/${id}/complete/`)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data || 'Failed to complete task' }
    }
  }

  // Add time to task
  const addTimeToTask = async (id, timeData) => {
    try {
      const response = await api.post(`/api/tasks/${id}/add_time/`, timeData)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data || 'Failed to add time to task' }
    }
  }

  // Clear current project
  const clearCurrentProject = () => {
    currentProject.value = null
  }

  // Clear error
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    projects,
    currentProject,
    loading,
    error,
    
    // Actions
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    createStage,
    updateStage,
    deleteStage,
    createTask,
    updateTask,
    deleteTask,
    startTask,
    completeTask,
    addTimeToTask,
    clearCurrentProject,
    clearError
  }
}) 