<template>
  <div class="projects">
    <div class="container mx-auto px-4 py-8">
      <!-- Header -->
      <div class="d-flex items-center justify-between mb-8">
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

      <!-- Projects List -->
      <div v-if="projects.length > 0" class="space-y-6">
        <ProjectsListSummary />
        <ProjectCard
          v-for="project in projects"
          :key="project.id"
          :project
        />
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
import ProjectsListSummary from "../components/projects/ProjectsListSummary.vue";
import ProjectCard from "../components/projects/ProjectCard.vue";

const projectStore = useProjectStore()

const projects = computed(() => projectStore.projects)
const loading = computed(() => projectStore.loading)
const error = computed(() => projectStore.error)

// Load projects
const loadProjects = async () => {
  await projectStore.fetchProjects()
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
  border-radius: 1rem;
  padding: 1rem;
}
.container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}


</style> 