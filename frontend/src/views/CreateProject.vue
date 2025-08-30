<template>
  <div class="create-project">
    <div class="container-fluid py-4">
      <div class="row justify-content-center">
        <div class="col-12 col-lg-8 col-xl-6">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h1 class="h2 text-dark mb-0">Create New Project</h1>
                <router-link
                  to="/projects"
                  class="btn btn-outline-secondary btn-sm"
                >
                  <i class="bi bi-arrow-left me-2"></i>Back to Projects
                </router-link>
              </div>

              <form @submit.prevent="handleSubmit">
                <!-- Project Name -->
                <div class="mb-3">
                  <label for="name" class="form-label">
                    Project Name <span class="text-danger">*</span>
                  </label>
                  <input
                    id="name"
                    v-model="form.name"
                    type="text"
                    required
                    class="form-control"
                    :class="{ 'is-invalid': errors.name }"
                    placeholder="Enter project name"
                  />
                  <div v-if="errors.name" class="invalid-feedback">
                    {{ errors.name }}
                  </div>
                </div>

                <!-- Project Description -->
                <div class="mb-3">
                  <label for="description" class="form-label">
                    Description
                  </label>
                  <textarea
                    id="description"
                    v-model="form.description"
                    rows="4"
                    class="form-control"
                    placeholder="Describe your project..."
                  ></textarea>
                </div>

                <!-- Project Status -->
                <div class="mb-4">
                  <label for="status" class="form-label">
                    Status
                  </label>
                  <select
                    id="status"
                    v-model="form.status"
                    class="form-select"
                  >
                    <option value="planning">Planning</option>
                    <option value="active">Active</option>
                    <option value="on_hold">On Hold</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>

                <!-- General Error Alert -->
                <div v-if="errors.general" class="alert alert-danger mb-4" role="alert">
                  <i class="bi bi-exclamation-triangle me-2"></i>
                  {{ errors.general }}
                </div>

                <!-- Submit Button -->
                <div class="d-flex justify-content-end gap-2">
                  <router-link
                    to="/projects"
                    class="btn btn-outline-secondary"
                  >
                    Cancel
                  </router-link>
                  <button
                    type="submit"
                    :disabled="loading"
                    class="btn btn-primary"
                  >
                    <span v-if="loading" class="d-flex align-items-center">
                      <div class="spinner-border spinner-border-sm me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                      </div>
                      Creating...
                    </span>
                    <span v-else>
                      <i class="bi bi-plus-circle me-2"></i>Create Project
                    </span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '../stores/project'

const router = useRouter()
const projectStore = useProjectStore()

const loading = ref(false)
const errors = reactive({})

const form = reactive({
  name: '',
  description: '',
  status: 'planning'
})

const handleSubmit = async () => {
  // Reset errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  // Validate form
  if (!form.name.trim()) {
    errors.name = 'Project name is required'
    return
  }

  loading.value = true

  try {
    const result = await projectStore.createProject(form)
    if (result.success) {
      // Redirect to the new project
      router.push(`/projects/${result.project.id}`)
    } else {
      // Handle API errors
      if (result.error) {
        if (typeof result.error === 'object') {
          Object.keys(result.error).forEach(key => {
            errors[key] = Array.isArray(result.error[key]) 
              ? result.error[key][0] 
              : result.error[key]
          })
        } else {
          errors.general = result.error
        }
      }
    }
  } catch (error) {
    console.error('Error creating project:', error)
    errors.general = 'An unexpected error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-project {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 0.75rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

@media (max-width: 767.98px) {
  .create-project {
    padding: 0.5rem;
  }
  
  .card-body {
    padding: 1.5rem !important;
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