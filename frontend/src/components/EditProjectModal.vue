<template>
  <BaseModal v-model="isOpen" @update:modelValue="handleClose">
    <template #header>
      Edit Project
    </template>

    <form @submit.prevent="handleSubmit">
      <!-- Project Name -->
      <div class="row mb-3">
        <div class="col-12 col-lg-3">
          <label for="name" class="form-label">
            Project Name *
          </label>
        </div>
        <div class="col-12 col-lg-9">
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
      </div>

      <!-- Project Description -->
      <div class="row mb-3">
        <div class="col-12 col-lg-3">
          <label for="description" class="form-label">
            Description
          </label>
        </div>
        <div class="col-12 col-lg-9">
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            class="form-control"
            placeholder="Enter project description"
          ></textarea>
        </div>
      </div>

      <!-- Project Status -->
      <div class="row mb-3">
        <div class="col-12 col-lg-3">
          <label for="status" class="form-label">
            Status
          </label>
        </div>
        <div class="col-12 col-lg-9">
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
      </div>

      <!-- Error Message -->
      <div v-if="errors.general" class="alert alert-danger" role="alert">
        {{ errors.general }}
      </div>
    </form>

    <template #footer>
      <button
        type="button"
        @click="handleClose"
        class="btn btn-secondary"
      >
        Cancel
      </button>
      <button
        type="submit"
        :disabled="loading"
        @click="handleSubmit"
        class="btn btn-primary"
      >
        <span v-if="loading" class="d-flex align-items-center">
          <div class="spinner-border spinner-border-sm me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          Saving...
        </span>
        <span v-else>Save Changes</span>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useProjectStore } from '../stores/project'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

const projectStore = useProjectStore()
const loading = ref(false)
const errors = reactive({})

const form = reactive({
  name: '',
  description: '',
  status: 'planning'
})

// Computed property for v-model
const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Initialize form with project data
onMounted(() => {
  if (props.project) {
    form.name = props.project.name || ''
    form.description = props.project.description || ''
    form.status = props.project.status || 'planning'
  }
})

const handleClose = () => {
  emit('update:modelValue', false)
}

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
    const result = await projectStore.updateProject(props.project.id, form)
    if (result.success) {
      emit('saved')
      handleClose()
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
    console.error('Error updating project:', error)
    errors.general = 'An unexpected error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script> 