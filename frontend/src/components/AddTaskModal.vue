<template>
  <BaseModal v-model="isOpen" @update:modelValue="handleClose">
    <template #header>
      Add New Task
    </template>

    <form @submit.prevent="handleSubmit" class="space-y-4 max-h-[60vh] overflow-y-auto">
      <!-- Task Name -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
          Task Name *
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

      <!-- Task Description -->
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

      <!-- Stage Selection -->
      <div>
        <label for="stage" class="block text-sm font-medium text-gray-700 mb-1">
          Stage (Optional)
        </label>
        <select
          id="stage"
          v-model="form.stage"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        >
          <option value="">No Stage (General Task)</option>
          <option v-for="stage in stages" :key="stage.id" :value="stage.id">
            {{ stage.name }}
          </option>
        </select>
      </div>

      <!-- Priority -->
      <div>
        <label for="priority" class="block text-sm font-medium text-gray-700 mb-1">
          Priority
        </label>
        <select
          id="priority"
          v-model="form.priority"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="urgent">Urgent</option>
        </select>
      </div>

      <!-- Status -->
      <div>
        <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
          Status
        </label>
        <select
          id="status"
          v-model="form.status"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        >
          <option value="not_started">Not Started</option>
          <option value="in_progress">In Progress</option>
          <option value="review">In Review</option>
          <option value="completed">Completed</option>
          <option value="blocked">Blocked</option>
        </select>
      </div>

      <!-- Time Estimates -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="estimated_hours" class="block text-sm font-medium text-gray-700 mb-1">
            Estimated Hours
          </label>
          <input
            id="estimated_hours"
            v-model.number="form.estimated_hours"
            type="number"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          />
        </div>
        <div>
          <label for="estimated_minutes" class="block text-sm font-medium text-gray-700 mb-1">
            Estimated Minutes
          </label>
          <select
            id="estimated_minutes"
            v-model.number="form.estimated_minutes"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          >
            <option value="0">0</option>
            <option value="15">15</option>
            <option value="30">30</option>
            <option value="45">45</option>
          </select>
        </div>
      </div>

      <!-- Timeline -->
      <div class="border-t pt-4">
        <h4 class="text-sm font-medium text-gray-700 mb-3">Timeline (Optional)</h4>
        
        <div class="grid grid-cols-1 gap-4">
          <div>
            <label for="planned_start_date" class="block text-sm font-medium text-gray-700 mb-1">
              Planned Start Date
            </label>
            <input
              id="planned_start_date"
              v-model="form.timeline.planned_start_date"
              type="datetime-local"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            />
          </div>
          
          <div>
            <label for="planned_due_date" class="block text-sm font-medium text-gray-700 mb-1">
              Planned Due Date
            </label>
            <input
              id="planned_due_date"
              v-model="form.timeline.planned_due_date"
              type="datetime-local"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            />
          </div>
        </div>
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
          Creating...
        </span>
        <span v-else>Create Task</span>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useProjectStore } from '../stores/project'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  projectId: {
    type: [String, Number],
    required: true
  },
  stages: {
    type: Array,
    default: () => []
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
  stage: '',
  priority: 'medium',
  status: 'not_started',
  estimated_hours: 0,
  estimated_minutes: 0,
  timeline: {
    planned_start_date: '',
    planned_due_date: ''
  },
  project: props.projectId
})

// Computed property for v-model
const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleSubmit = async () => {
  // Reset errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  // Validate form
  if (!form.name.trim()) {
    errors.name = 'Task name is required'
    return
  }

  // Prepare form data
  const formData = { ...form }
  
  // Handle stage field - only include if it's not empty
  if (formData.stage === '') {
    delete formData.stage
  }
  
  // Handle timeline - only include if dates are set
  if (!formData.timeline.planned_start_date && !formData.timeline.planned_due_date) {
    delete formData.timeline
  }

  loading.value = true

  try {
    const result = await projectStore.createTask(formData)
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
    console.error('Error creating task:', error)
    errors.general = 'An unexpected error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script> 