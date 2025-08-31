<script setup>

import {useProjectStore} from "../../stores/project.js";

import { computed } from 'vue'
const projectStore = useProjectStore()

const projects = computed(() => projectStore.projects)

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
    // Only include incomplete projects
    if (project.status !== 'completed') {
      if (project.total_estimated_hours) {
        totalHours += project.total_estimated_hours
      }
      if (project.total_estimated_minutes) {
        totalMinutes += project.total_estimated_minutes
      }
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

</script>

<template>

  <!-- Summary Stats -->
  <div v-if="projects.length > 0" class="card shadow-sm border-0 mb-4">
    <div class="card-body p-4">
      <h2 class="card-title h5 text-dark mb-4">Project Summary</h2>
      <div class="row g-3">
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h3 fw-bold text-primary mb-1">{{ totalProjects }}</div>
            <div class="small text-muted">Total Projects</div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h3 fw-bold text-success mb-1">{{ totalTasks }}</div>
            <div class="small text-muted">Total Tasks</div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h3 fw-bold text-warning mb-1">{{ completedTasks }}</div>
            <div class="small text-muted">Completed Tasks</div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="text-center">
            <div class="h3 fw-bold text-info mb-1">{{ totalEstimatedTime }}</div>
            <div class="small text-muted">Est. Time (Incomplete)</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom styles for enhanced visual appeal */
.card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 0.75rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.h3 {
  font-size: 2rem;
  line-height: 1.2;
}

@media (max-width: 767.98px) {
  .h3 {
    font-size: 1.5rem;
  }
  
  .card-body {
    padding: 1rem !important;
  }
}
</style>