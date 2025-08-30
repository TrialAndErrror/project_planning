<template>
  <div class="projects">
    <div class="container mx-auto px-4 py-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">My Projects</h1>
          <p class="text-gray-600 mt-2">Manage and track your project planning</p>
        </div>
        <router-link
          to="/projects/create"
          class="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          + New Project
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <div class="text-red-600 text-lg mb-4">{{ error }}</div>
        <button @click="loadProjects" class="text-blue-600 hover:text-blue-800">
          Try Again
        </button>
      </div>



      <!-- Summary Stats -->
      <div v-if="projects.length > 0" class="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Project Summary</h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">{{ totalProjects }}</div>
            <div class="text-sm text-gray-600">Total Projects</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600">{{ totalTasks }}</div>
            <div class="text-sm text-gray-600">Total Tasks</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-orange-600">{{ completedTasks }}</div>
            <div class="text-sm text-gray-600">Completed Tasks</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-600">{{ totalEstimatedTime }}</div>
            <div class="text-sm text-gray-600">Est. Time Remaining</div>
          </div>
        </div>
      </div>

      <!-- Projects List -->
      <div v-if="projects.length > 0" class="space-y-6">
        <div
          v-for="project in projects"
          :key="project.id"
          class="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
        >
          <div class="p-6">
            <!-- Project Header -->
            <div class="flex items-start justify-between mb-6">
              <div class="flex-1">
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">
                  {{ project.name }}
                </h3>
                <p class="text-gray-600 text-base">
                  {{ project.description || 'No description' }}
                </p>
              </div>
              <div class="flex items-center space-x-4">
                <span class="px-3 py-1 rounded-full text-sm font-medium" :class="getStatusClasses(project.status)">
                  {{ getStatusLabel(project.status) }}
                </span>
                <div class="text-xs text-gray-500">
                  Created {{ formatDate(project.created_at) }}
                </div>
              </div>
            </div>

            <!-- Project Stats Row -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
              <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">{{ project.stage_count }}</div>
                <div class="text-sm text-gray-600">Stages</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-green-600">{{ project.task_count }}</div>
                <div class="text-sm text-gray-600">Tasks</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-orange-600">{{ project.completed_task_count }}</div>
                <div class="text-sm text-gray-600">Completed</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-purple-600">
                  {{ formatEstimatedTime(project.total_estimated_hours, project.total_estimated_minutes) }}
                </div>
                <div class="text-sm text-gray-600">Est. Time</div>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mb-6">
              <div class="flex justify-between text-sm text-gray-600 mb-2">
                <span>Progress</span>
                <span>{{ project.progress_percentage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-3">
                <div
                  class="bg-blue-600 h-3 rounded-full transition-all duration-300"
                  :style="{ width: `${project.progress_percentage}%` }"
                ></div>
              </div>
            </div>

            <!-- Project Actions -->
            <div class="flex items-center justify-end space-x-3 pt-4 border-t border-gray-200">
              <router-link
                :to="`/projects/${project.id}`"
                class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
              >
                View Project
              </router-link>
              <button
                @click="deleteProject(project.id)"
                class="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors duration-200"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <div class="max-w-md mx-auto">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No projects yet</h3>
          <p class="mt-2 text-gray-600">Get started by creating your first project.</p>
          <div class="mt-6">
            <router-link
              to="/projects/create"
              class="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Create Your First Project
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useProjectStore } from '../stores/project'

const projectStore = useProjectStore()

const projects = computed(() => projectStore.projects)
const loading = computed(() => projectStore.loading)
const error = computed(() => projectStore.error)

// Summary statistics
const totalProjects = computed(() => projects.value.length)

const totalTasks = computed(() => {
  return projects.value.reduce((total, project) => total + (project.task_count || 0), 0)
})

const completedTasks = computed(() => {
  return projects.value.reduce((total, project) => total + (project.completed_task_count || 0), 0)
})

const totalEstimatedTime = computed(() => {
  let totalHours = 0
  let totalMinutes = 0
  
  projects.value.forEach(project => {
    if (project.total_estimated_hours) {
      totalHours += project.total_estimated_hours
    }
    if (project.total_estimated_minutes) {
      totalMinutes += project.total_estimated_minutes
    }
  })
  
  // Convert minutes to hours
  totalHours += Math.floor(totalMinutes / 60)
  totalMinutes = totalMinutes % 60
  
  if (totalHours > 0 && totalMinutes > 0) {
    return `${totalHours}h ${totalMinutes}m`
  } else if (totalHours > 0) {
    return `${totalHours}h`
  } else if (totalMinutes > 0) {
    return `${totalMinutes}m`
  } else {
    return '0h'
  }
})

// Load projects
const loadProjects = async () => {
  await projectStore.fetchProjects()
}

// Helper functions
const getStatusLabel = (status) => {
  const labels = {
    planning: 'Planning',
    active: 'Active',
    on_hold: 'On Hold',
    completed: 'Completed',
    cancelled: 'Cancelled'
  }
  return labels[status] || status
}

const getStatusClasses = (status) => {
  const classes = {
    planning: 'bg-yellow-100 text-yellow-800',
    active: 'bg-green-100 text-green-800',
    on_hold: 'bg-orange-100 text-orange-800',
    completed: 'bg-blue-100 text-blue-800',
    cancelled: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatEstimatedTime = (hours, minutes) => {
  if (!hours && !minutes) return '0h'
  
  const totalHours = (hours || 0) + Math.floor((minutes || 0) / 60)
  const remainingMinutes = (minutes || 0) % 60
  
  if (totalHours > 0 && remainingMinutes > 0) {
    return `${totalHours}h ${remainingMinutes}m`
  } else if (totalHours > 0) {
    return `${totalHours}h`
  } else if (remainingMinutes > 0) {
    return `${remainingMinutes}m`
  } else {
    return '0h'
  }
}

const deleteProject = async (projectId) => {
  if (confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
    const result = await projectStore.deleteProject(projectId)
    if (!result.success) {
      alert('Failed to delete project. Please try again.')
    }
  }
}

// Load projects on mount
onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.projects {
  min-height: 100vh;
  background-color: #f9fafb;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 