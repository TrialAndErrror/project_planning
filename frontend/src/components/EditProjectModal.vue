<template>
  <BaseModal v-model="isOpen" @update:modelValue="handleClose">
    <template #header>
      Edit Project
    </template>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Project Name -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
          Project Name *
        </label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          :class="{ 'border-red-500': errors.name }"
        />
        <p v-if="errors.name" class="mt-1 text-sm text-red-600">
          {{ errors.name }}
        </p>
      </div>

      <!-- Project Description -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          v-model="form.description"
          rows="3"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        ></textarea>
      </div>

      <!-- Project Status -->
      <div>
        <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
          Status
        </label>
        <select
          id="status"
          v-model="form.status"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        >
          <option value="planning">Planning</option>
          <option value="active">Active</option>
          <option value="on_hold">On Hold</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      <!-- Error Message -->
      <div v-if="errors.general" class="text-red-600 text-sm bg-red-50 p-3 rounded-md border border-red-200">
        {{ errors.general }}
      </div>
    </form>

    <template #footer>
      <button
        type="button"
        @click="handleClose"
        class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
      >
        Cancel
      </button>
      <button
        type="submit"
        :disabled="loading"
        @click="handleSubmit"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
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