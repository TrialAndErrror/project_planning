<script setup lang="ts">
import { useProjectStore } from "@/stores/project"
import { computed } from 'vue'
import type { Project } from '@/types'

const projectStore = useProjectStore()

const projects = computed(() => projectStore.projects)

// Summary statistics
const totalProjects = computed(() => projects.value.length)

const totalTasks = computed(() => {
  return projects.value.reduce((total: number, project: Project) => {
    return total + project.stages.reduce((stageTotal: number, stage: any) => {
      return stageTotal + stage.tasks.length
    }, 0)
  }, 0)
})

const completedTasks = computed(() => {
  return projects.value.reduce((total: number, project: Project) => {
    return total + project.stages.reduce((stageTotal: number, stage: any) => {
      return stageTotal + stage.tasks.filter((task: any) => task.status === 'done').length
    }, 0)
  }, 0)
})

const totalEstimatedTime = computed(() => {
  // Since we don't have estimated time in the current data structure,
  // we'll return a placeholder for now
  return '0h'
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