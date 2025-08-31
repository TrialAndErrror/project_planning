<template>
  <BaseModal v-model="isOpen" @update:modelValue="handleClose">
    <template #header>
      Add New Task
    </template>

    <form @submit.prevent="handleSubmit" class="max-h-[60vh] overflow-x-hidden overflow-y-auto">
      <!-- Task Name -->
      <div class="row mb-3">
        <div class="col-12 col-lg-3">
          <label for="name" class="form-label">
            Task Name *
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
            placeholder="Enter task name"
          />
          <div v-if="errors.name" class="invalid-feedback">
            {{ errors.name }}
          </div>
        </div>
      </div>

      <!-- Stage Selection -->
      <div class="row mb-3">
        <div class="col-12 col-lg-3">
          <label for="stage" class="form-label">
            Stage (Optional)
          </label>
        </div>
        <div class="col-12 col-lg-9">
          <select
            id="stage"
            v-model="form.stage"
            class="form-select"
          >
            <option value="">No Stage (General Task)</option>
            <option v-for="stage in stages" :key="stage.id" :value="stage.id">
              {{ stage.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Task Description -->
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
            placeholder="Enter task description"
          ></textarea>
        </div>
      </div>

      <!-- Task Details Collapsible Section -->
      <div class="card mb-3">
        <div class="card-header" role="button" @click="toggleTaskDetails" style="cursor: pointer;">
          <div class="d-flex justify-content-between align-items-center">
            <span>Task Details (Optional)</span>
            <i class="bi" :class="showTaskDetails ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
        </div>
        <div v-show="showTaskDetails" class="card-body">
          <!-- Priority -->
          <div class="row mb-3">
            <div class="col-12 col-lg-3">
              <label for="priority" class="form-label">
                Priority
              </label>
            </div>
            <div class="col-12 col-lg-9">
              <select
                id="priority"
                v-model="form.priority"
                class="form-select"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>

          <!-- Status -->
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
                <option value="not_started">Not Started</option>
                <option value="in_progress">In Progress</option>
                <option value="review">In Review</option>
                <option value="completed">Completed</option>
                <option value="blocked">Blocked</option>
              </select>
            </div>
          </div>

          <!-- Time Estimates -->
          <div class="row mb-3">
            <div class="col-12 col-lg-3">
              <label class="form-label">Time Estimates</label>
            </div>
            <div class="col-12 col-lg-9">
              <div class="row">
                <div class="col-6">
                  <label for="estimated_hours" class="form-label">
                    Hours
                  </label>
                  <input
                    id="estimated_hours"
                    v-model.number="form.estimated_hours"
                    type="number"
                    min="0"
                    class="form-control"
                    placeholder="0"
                  />
                </div>
                <div class="col-6">
                  <label for="estimated_minutes" class="form-label">
                    Minutes
                  </label>
                  <select
                    id="estimated_minutes"
                    v-model.number="form.estimated_minutes"
                    class="form-select"
                  >
                    <option value="0">0</option>
                    <option value="15">15</option>
                    <option value="30">30</option>
                    <option value="45">45</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Timeline Collapsible Section -->
      <div class="card mb-3">
        <div class="card-header" role="button" @click="toggleTimeline" style="cursor: pointer;">
          <div class="d-flex justify-content-between align-items-center">
            <span>Timeline (Optional)</span>
            <i class="bi" :class="showTimeline ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
        </div>
        <div v-show="showTimeline" class="card-body">
          <div class="row mb-3">
            <div class="col-12 col-lg-3">
              <label for="planned_start_date" class="form-label">
                Planned Start Date
              </label>
            </div>
            <div class="col-12 col-lg-9">
              <input
                id="planned_start_date"
                v-model="form.timeline.planned_start_date"
                type="datetime-local"
                class="form-control"
              />
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-12 col-lg-3">
              <label for="planned_due_date" class="form-label">
                Planned Due Date
              </label>
            </div>
            <div class="col-12 col-lg-9">
              <input
                id="planned_due_date"
                v-model="form.timeline.planned_due_date"
                type="datetime-local"
                class="form-control"
              />
            </div>
          </div>
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
        class="btn btn-success"
      >
        <span v-if="loading" class="d-flex align-items-center">
          <div class="spinner-border spinner-border-sm me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
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
const showTaskDetails = ref(false)
const showTimeline = ref(false)

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

const toggleTaskDetails = () => {
  showTaskDetails.value = !showTaskDetails.value
}

const toggleTimeline = () => {
  showTimeline.value = !showTimeline.value
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

<style>

</style>