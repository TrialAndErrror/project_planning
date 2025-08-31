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

<script setup>
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
}

/* Custom modal sizes if needed */
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

/* Prevent body scroll when modal is open */
:global(body.modal-open) {
  overflow: hidden;
  padding-right: 0;
}
</style>
