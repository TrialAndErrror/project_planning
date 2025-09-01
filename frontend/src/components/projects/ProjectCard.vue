<script setup lang="ts">
import { useProjectStore } from '@/stores/project'
import { useRouter } from 'vue-router'
import type { Project } from '@/types'

// Define props
interface Props {
  project: Project
}

const props = defineProps<Props>()

const projectStore = useProjectStore()
const router = useRouter()

// Helper functions - using store functions
const getStatusLabel = projectStore.getStatusLabel
const getStatusClasses = projectStore.getStatusBadgeClasses

const formatDate = (dateString: string): string => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatEstimatedTime = (hours?: number, minutes?: number): string => {
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

const navigateToProject = (): void => {
  router.push(`/projects/${props.project.id}`)
}

const deleteProject = async (projectId: number): Promise<void> => {
  if (confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
    const result = await projectStore.deleteProject(projectId)
    if (!result.success) {
      alert('Failed to delete project. Please try again.')
    }
  }
}

</script>

<template>

  <div v-if="project" class="card shadow-sm border-0 mb-4 project-card">
    <div 
      class="card-body p-4 project-card-content"
      @click="navigateToProject"
      style="cursor: pointer;"
    >
      <!-- Project Header -->
      <div class="d-flex justify-content-between align-items-start mb-4">
        <div class="flex-grow-1 me-3">
          <h3 class="card-title h4 text-dark mb-2">
            {{ project.title || 'Untitled Project' }}
          </h3>
          <p class="text-muted mb-0">
            {{ project.description || 'No description' }}
          </p>
        </div>
        <div class="d-flex flex-column align-items-end">
          <small class="text-muted">
            Created {{ formatDate(project.created_at) }}
          </small>
        </div>
      </div>

      <!-- Project Stats Row -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h4 fw-bold text-primary mb-1">{{ project.stages?.length || 0 }}</div>
            <div class="small text-muted">Stages</div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h4 fw-bold text-success mb-1">
              {{ project.stages?.reduce((total: number, stage: any) => total + stage.tasks.length, 0) || 0 }}
            </div>
            <div class="small text-muted">Tasks</div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h4 fw-bold text-warning mb-1">
              {{ project.stages?.reduce((total: number, stage: any) => 
                total + stage.tasks.filter((task: any) => task.status === 'done').length, 0) || 0 }}
            </div>
            <div class="small text-muted">Completed</div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h4 fw-bold text-info mb-1">
              {{ project.stages?.length || 0 }}
            </div>
            <div class="small text-muted">Stages</div>
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="mb-4">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="small text-muted">Progress</span>
          <span class="small text-muted">
            {{ project.stages?.length ? 
              Math.round((project.stages.reduce((total: number, stage: any) => 
                total + stage.tasks.filter((task: any) => task.status === 'done').length, 0) / 
                project.stages.reduce((total: number, stage: any) => total + stage.tasks.length, 0)) * 100) || 0 : 0 }}%
          </span>
        </div>
        <div class="progress" style="height: 8px;">
          <div
              class="progress-bar bg-primary"
              :style="{ width: `${project.stages?.length ? 
                Math.round((project.stages.reduce((total, stage) => 
                  total + stage.tasks.filter(task => task.status === 'done').length, 0) / 
                  project.stages.reduce((total, stage) => total + stage.tasks.length, 0)) * 100) || 0 : 0}%` }"
              role="progressbar"
              :aria-valuenow="project.stages?.length ? 
                Math.round((project.stages.reduce((total, stage) => 
                  total + stage.tasks.filter(task => task.status === 'done').length, 0) / 
                  project.stages.reduce((total, stage) => total + stage.tasks.length, 0)) * 100) || 0 : 0"
              aria-valuemin="0"
              aria-valuemax="100"
          ></div>
        </div>
      </div>

      <!-- Project Actions -->
      <div class="d-flex justify-content-end gap-2 pt-3 border-top">
        <router-link
            :to="`/projects/${project.id}`"
            class="btn btn-primary btn-sm"
        >
          View Project
        </router-link>
        <button
            @click.stop="deleteProject(project.id)"
            class="btn btn-outline-danger btn-sm"
        >
          Delete
        </button>
      </div>
    </div>
  </div>

  <!-- Loading/Error State -->
  <div v-else class="card shadow-sm border-0 mb-4">
    <div class="card-body p-4">
      <div class="text-center text-muted">
        <div class="spinner-border spinner-border-sm me-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        Loading project...
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom styles for enhanced visual appeal */
.project-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 0.75rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.project-card-content {
  transition: background-color 0.2s ease-in-out;
}

.project-card-content:hover {
  background-color: #c5e1c5 !important;
}

.h4 {
  font-size: 1.5rem;
  line-height: 1.2;
}

.progress {
  border-radius: 0.5rem;
  background-color: #e9ecef;
}

.progress-bar {
  border-radius: 0.5rem;
  transition: width 0.3s ease;
}

.badge {
  font-weight: 500;
  font-size: 0.75rem;
}

/* Status Badge Styles */
.status-planning,
.status-on-hold {
  background-color: rgba(255, 193, 7, 0.1) !important;
  color: #ffc107 !important;
}

.status-active {
  background-color: rgba(25, 135, 84, 0.1) !important;
  color: #198754 !important;
}

.status-completed {
  background-color: rgba(108, 117, 125, 0.2) !important;
  color: #000000 !important;
}

.status-cancelled {
  background-color: rgba(220, 53, 69, 0.1) !important;
  color: #dc3545 !important;
}

@media (max-width: 767.98px) {
  .h4 {
    font-size: 1.25rem;
  }

  .card-body {
    padding: 1rem !important;
  }

  .d-flex.justify-content-between.align-items-start {
    flex-direction: column;
    align-items: flex-start !important;
  }

  .d-flex.flex-column.align-items-end {
    align-items: flex-start !important;
    margin-top: 1rem;
  }
}
</style>