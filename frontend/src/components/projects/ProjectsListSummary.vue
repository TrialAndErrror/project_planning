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

</script>

<template>

  <!-- Summary Stats -->
  <div v-if="projects.length > 0" class="project-summary-container bg-white rounded-lg shadow-lg p-6 mb-8">
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
</template>

<style scoped>
.project-summary-container {
  display: grid;
  grid-template-columns: 1fr 4fr;
}

</style>