<template>
  <div class="projects">
    <div class="container-fluid py-4">
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 class="h2 text-dark mb-2">My Projects</h1>
          <p class="text-muted mb-0">Manage and track your project planning</p>
        </div>
        <router-link
          to="/projects/create"
          class="btn btn-primary"
        >
          <i class="bi bi-plus-circle me-2"></i>New Project
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height: 300px;">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-5">
        <div class="alert alert-danger d-inline-block" role="alert">
          <i class="bi bi-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
        <div class="mt-3">
          <button @click="loadProjects" class="btn btn-outline-primary">
            <i class="bi bi-arrow-clockwise me-2"></i>Try Again
          </button>
        </div>
      </div>

      <!-- Projects List -->
      <div v-if="projects.length > 0">
        <ProjectsListSummary />
        <div class="row g-4">
          <div class="col-12">
            <ProjectCard
              v-for="project in projects"
              :key="project.id"
              :project="project"
            />
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-5">
        <div class="card border-0 shadow-sm mx-auto" style="max-width: 400px;">
          <div class="card-body p-5">
            <div class="empty-state-icon mb-4">
              <i class="bi bi-folder-x text-muted"></i>
            </div>
            <h3 class="h5 text-dark mb-3">No projects yet</h3>
            <p class="text-muted mb-4">Get started by creating your first project.</p>
            <router-link
              to="/projects/create"
              class="btn btn-primary btn-lg"
            >
              <i class="bi bi-plus-circle me-2"></i>Create Your First Project
            </router-link>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useProjectStore } from '@/stores/project'
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
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1rem;
}

.empty-state-icon {
  font-size: 4rem;
  opacity: 0.6;
}

.empty-state-icon i {
  font-size: 4rem;
}

@media (max-width: 767.98px) {
  .projects {
    padding: 0.5rem;
  }
  
  .d-flex.justify-content-between.align-items-center {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 1rem;
  }
  
  .btn {
    width: 100%;
  }
}
</style> 