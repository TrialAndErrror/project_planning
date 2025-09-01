import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios, { AxiosInstance } from 'axios'
import type { Project, Stage, Task, ProjectForm, StageForm, TaskForm } from '@/types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create a local axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)
  
  // UI State for expandable sections
  const expandedStages = ref<Set<number>>(new Set())
  const expandedTasks = ref<Set<number>>(new Set())

  // Set auth token in axios headers dynamically
  const setAuthToken = (): void => {
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
      const response = await api.get<Project[]>('/api/projects/')
      projects.value = response.data
      return { success: true, projects: response.data }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to fetch projects'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Get single project
  const fetchProject = async (id: number) => {
    loading.value = true
    error.value = null
    
    try {
      setAuthToken()
      const response = await api.get<Project>(`/api/projects/${id}/`)
      currentProject.value = response.data
      return { success: true, project: response.data }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to fetch project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Create project
  const createProject = async (projectData: ProjectForm) => {
    loading.value = true
    error.value = null
    
    try {
      setAuthToken()
      const response = await api.post<Project>('/api/projects/', projectData)
      const newProject = response.data
      projects.value.unshift(newProject)
      return { success: true, project: newProject }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to create project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Update project
  const updateProject = async (id: number, projectData: ProjectForm) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.put<Project>(`/api/projects/${id}/`, projectData)
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
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to update project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Delete project
  const deleteProject = async (id: number) => {
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
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to delete project'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Create stage
  const createStage = async (stageData: StageForm & { project: number }) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post<Stage>('/api/stages/', stageData)
      const newStage = response.data
      
      // Add to current project if it exists
      if (currentProject.value && currentProject.value.id === stageData.project) {
        currentProject.value.stages.push(newStage)
      }
      
      return { success: true, stage: newStage }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to create stage'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Update stage
  const updateStage = async (id: number, stageData: StageForm) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.put<Stage>(`/api/stages/${id}/`, stageData)
      const updatedStage = response.data
      
      // Update in current project
      if (currentProject.value) {
        const stageIndex = currentProject.value.stages.findIndex(s => s.id === id)
        if (stageIndex !== -1) {
          currentProject.value.stages[stageIndex] = updatedStage
        }
      }
      
      return { success: true, stage: updatedStage }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to update stage'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Delete stage
  const deleteStage = async (id: number) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/api/stages/${id}/`)
      
      // Remove from current project
      if (currentProject.value) {
        currentProject.value.stages = currentProject.value.stages.filter(s => s.id !== id)
      }
      
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to delete stage'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Create task
  const createTask = async (taskData: TaskForm & { project: number }) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post<Task>('/api/tasks/', taskData)
      const newTask = response.data
      
      // Add to current project
      if (currentProject.value && currentProject.value.id === taskData.project) {
        // Find the stage and add the task to it
        const stage = currentProject.value.stages.find(s => s.id === taskData.stage)
        if (stage) {
          stage.tasks.push(newTask)
        }
      }
      
      return { success: true, task: newTask }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to create task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Update task
  const updateTask = async (id: number, taskData: Partial<TaskForm>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.put<Task>(`/api/tasks/${id}/`, taskData)
      const updatedTask = response.data
      
      // Update in current project
      if (currentProject.value) {
        // Find the task in any stage and update it
        for (const stage of currentProject.value.stages) {
          const taskIndex = stage.tasks.findIndex(t => t.id === id)
          if (taskIndex !== -1) {
            stage.tasks[taskIndex] = updatedTask
            break
          }
        }
      }
      
      return { success: true, task: updatedTask }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to update task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Delete task
  const deleteTask = async (id: number) => {
    loading.value = true
    error.value = null
    
    try {
      await api.delete(`/api/tasks/${id}/`)
      
      // Remove from current project
      if (currentProject.value) {
        for (const stage of currentProject.value.stages) {
          stage.tasks = stage.tasks.filter(t => t.id !== id)
        }
      }
      
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data || 'Failed to delete task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Start task
  const startTask = async (id: number) => {
    try {
      const response = await api.post(`/api/tasks/${id}/start/`)
      return { success: true, data: response.data }
    } catch (err: any) {
      return { success: false, error: err.response?.data || 'Failed to start task' }
    }
  }

  // Complete task
  const completeTask = async (id: number) => {
    try {
      const response = await api.post(`/api/tasks/${id}/complete/`)
      return { success: true, data: response.data }
    } catch (err: any) {
      return { success: false, error: err.response?.data || 'Failed to complete task' }
    }
  }

  // Add time to task
  const addTimeToTask = async (id: number, timeData: { hours: number; minutes: number }) => {
    try {
      const response = await api.post(`/api/tasks/${id}/add_time/`, timeData)
      return { success: true, data: response.data }
    } catch (err: any) {
      return { success: false, error: err.response?.data || 'Failed to add time to task' }
    }
  }

  // Clear current project
  const clearCurrentProject = (): void => {
    currentProject.value = null
  }

  // Clear error
  const clearError = (): void => {
    error.value = null
  }

  // Helper functions
  const getStatusLabel = (status: string): string => {
    return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  }

  const getStatusBadgeClasses = (status: string): string => {
    return `status-${status.replace('_', '-')}`
  }

  const getPriorityBadgeClasses = (priority: string): string => {
    return `priority-${priority}`
  }

  // Task filtering functions
  const getTasksForStage = (stageId: number): Task[] => {
    if (!currentProject.value) return []
    const stage = currentProject.value.stages.find(s => s.id === stageId)
    return stage ? stage.tasks : []
  }

  const getTasksWithoutStage = (): Task[] => {
    if (!currentProject.value) return []
    // Get all tasks that don't have a stage assigned
    return currentProject.value.tasks?.filter(task => !task.stage || task.stage === null) || []
  }



  // Toggle methods for expandable sections
  const toggleStage = (stageId: number): void => {
    if (expandedStages.value.has(stageId)) {
      expandedStages.value.delete(stageId)
    } else {
      expandedStages.value.add(stageId)
    }
  }

  const toggleTask = (taskId: number): void => {
    if (expandedTasks.value.has(taskId)) {
      expandedTasks.value.delete(taskId)
    } else {
      expandedTasks.value.add(taskId)
    }
  }

  const isStageExpanded = (stageId: number): boolean => {
    return expandedStages.value.has(stageId)
  }

  const isTaskExpanded = (taskId: number): boolean => {
    return expandedTasks.value.has(taskId)
  }



  return {
    // State
    projects,
    currentProject,
    loading,
    error,
    expandedStages,
    expandedTasks,
    
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
    clearError,
    
    // Helper functions
    getStatusLabel,
    getStatusBadgeClasses,
    getPriorityBadgeClasses,
    getTasksForStage,
    getTasksWithoutStage,
    
    // UI State management
    toggleStage,
    toggleTask,
    isStageExpanded,
    isTaskExpanded,
    

  }
})
