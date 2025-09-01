<template>
  <BaseModal v-model="isOpen" @update:modelValue="handleClose">
    <template #header>
      Edit Stage
    </template>

    <form @submit.prevent="handleSubmit">
      <!-- Stage Name -->
      <div class="row mb-3">
        <div class="col-12 col-lg-3">
          <label for="name" class="form-label">
            Stage Name *
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
            placeholder="Enter stage name"
          />
          <div v-if="errors.name" class="invalid-feedback">
            {{ errors.name }}
          </div>
        </div>
      </div>

      <!-- Stage Description -->
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
            placeholder="Enter stage description"
          ></textarea>
        </div>
      </div>

      <!-- Stage Order -->
      <div class="row mb-3">
        <div class="col-12 col-lg-3">
          <label for="order" class="form-label">
            Order
          </label>
        </div>
        <div class="col-12 col-lg-9">
          <input
            id="order"
            v-model.number="form.order"
            type="number"
            min="0"
            class="form-control"
            placeholder="0"
          />
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

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useProjectStore } from '@/stores/project'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  stage: {
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
  order: 0
})

// Computed property for v-model
const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Initialize form with stage data
const initializeForm = () => {
  if (props.stage) {
    form.name = props.stage.name || ''
    form.description = props.stage.description || ''
    form.order = props.stage.order || 0
  }
}

// Watch for changes to the stage prop
watch(() => props.stage, initializeForm, { immediate: true })

// Also initialize on mount as fallback
onMounted(initializeForm)

const resetForm = () => {
  form.name = ''
  form.description = ''
  form.order = 0
  Object.keys(errors).forEach(key => delete errors[key])
}

const handleClose = () => {
  resetForm()
  emit('update:modelValue', false)
}

const handleSubmit = async () => {
  // Reset errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  // Validate form
  if (!form.name.trim()) {
    errors.name = 'Stage name is required'
    return
  }

  loading.value = true

  try {
    const result = await projectStore.updateStage(props.stage.id, form)
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
    console.error('Error updating stage:', error)
    errors.general = 'An unexpected error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script> 