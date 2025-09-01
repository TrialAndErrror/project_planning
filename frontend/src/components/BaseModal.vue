<template>
  <Teleport to="body">
    <Transition name="modal-backdrop" appear>
      <div 
        v-if="modelValue"
        class="modal fade show d-block"
        tabindex="-1"
        @click="handleBackdropClick"
      >
        <!-- Backdrop -->
        <div class="modal-backdrop fade show" style="z-index: 1050;"></div>
        
        <!-- Modal Container -->
        <div class="modal-dialog modal-dialog-centered" style="z-index: 1055;">
          <div 
            class="modal-content"
            @click.stop
          >
            <!-- Modal Header -->
            <div class="modal-header">
              <h5 class="modal-title">
                <slot name="header"></slot>
              </h5>
              <button
                @click="$emit('update:modelValue', false)"
                class="btn-close"
                type="button"
                aria-label="Close"
              ></button>
            </div>

            <!-- Modal Body -->
            <div class="modal-body">
              <slot></slot>
            </div>

            <!-- Modal Footer -->
            <div v-if="$slots.footer" class="modal-footer">
              <slot name="footer"></slot>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

const handleBackdropClick = () => {
  if (props.closeOnBackdrop) {
    emit('update:modelValue', false)
  }
}

// Handle escape key
const handleEscape = (event) => {
  if (event.key === 'Escape' && props.modelValue) {
    emit('update:modelValue', false)
  }
}

// Prevent body scroll when modal is open
const preventBodyScroll = () => {
  if (props.modelValue) {
    document.body.classList.add('modal-open')
  } else {
    document.body.classList.remove('modal-open')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
  preventBodyScroll()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  document.body.classList.remove('modal-open')
})

// Watch for modelValue changes to handle body scroll
import { watch } from 'vue'
watch(() => props.modelValue, preventBodyScroll)
</script>

<style scoped>
/* Custom modal transitions to work with Bootstrap */
.modal-backdrop-enter-active,
.modal-backdrop-leave-active {
  transition: opacity 0.3s ease;
}

.modal-backdrop-enter-from,
.modal-backdrop-leave-to {
  opacity: 0;
}

/* Ensure proper z-index hierarchy */
.modal {
  z-index: 1055 !important;
}

.modal-backdrop {
  z-index: 1050 !important;
}

.modal-dialog {
  z-index: 1055 !important;
  position: relative;
}

.modal-content {
  position: relative;
  z-index: 1056 !important;
  border: none;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  overflow-x: hidden;
}

/* Custom modal header to match navbar */
.modal-header {
  color: white !important;
  border-bottom: 1px solid #34495e;
  border-radius: 8px 8px 0 0;
  padding: 1rem 1.5rem;
}

.modal-title {
  color: white !important;
  font-weight: 600;
  font-size: 1.25rem;
}

.btn-close {
  filter: invert(1) brightness(100);
  opacity: 0.8;
}

.btn-close:hover {
  opacity: 1;
}

/* Modal body styling */
.modal-body {
  padding: 1.5rem;
  background-color: #ffffff;
  overflow-x: hidden;
}

/* Modal footer styling */
.modal-footer {
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
  padding: 1rem 1.5rem;
  border-radius: 0 0 8px 8px;
}

/* Custom modal sizes */
.modal-dialog {
  max-width: 500px;
}

@media (min-width: 768px) {
  .modal-dialog {
    max-width: 600px;
  }
}

@media (min-width: 992px) {
  .modal-dialog {
    max-width: 700px;
  }
}

/* Bootstrap form styling enhancements */
.modal-body .form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
}

.modal-body .form-control {
  border-radius: 6px;
  border: 1px solid #ced4da;
  padding: 0.75rem 1rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.modal-body .form-control:focus {
  border-color: #2c3e50;
  box-shadow: 0 0 0 0.2rem rgba(44, 62, 80, 0.25);
}

.modal-body .form-select {
  border-radius: 6px;
  border: 1px solid #ced4da;
  padding: 0.75rem 1rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.modal-body .form-select:focus {
  border-color: #2c3e50;
  box-shadow: 0 0 0 0.2rem rgba(44, 62, 80, 0.25);
}

.modal-body textarea.form-control {
  min-height: 100px;
  resize: vertical;
}

/* Button styling in modal footer */
.modal-footer .btn {
  border-radius: 6px;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
  transition: all 0.15s ease-in-out;
}

.modal-footer .btn-primary {
  background-color: #2c3e50;
  border-color: #2c3e50;
}

.modal-footer .btn-primary:hover {
  background-color: #34495e;
  border-color: #34495e;
}

.modal-footer .btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.modal-footer .btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.modal-footer .btn-success {
  background-color: #198754;
  border-color: #198754;
}

.modal-footer .btn-success:hover {
  background-color: #157347;
  border-color: #146c43;
}

/* Prevent body scroll when modal is open */
:global(body.modal-open) {
  overflow: hidden;
  padding-right: 0;
}
</style>
