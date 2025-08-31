<template>
  <Transition name="modal-backdrop" appear>
    <div 
      v-if="modelValue"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click="handleBackdropClick"
    >
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>
      
      <!-- Modal Container -->
      <div class="flex min-h-full items-center justify-center p-4">
        <Transition name="modal-content" appear>
          <div 
            class="relative w-full max-w-md transform overflow-hidden rounded-lg bg-white shadow-xl transition-all"
            @click.stop
          >
            <!-- Modal Header -->
            <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4">
              <h3 class="text-lg font-semibold text-gray-900">
                <slot name="header"></slot>
              </h3>
              <button
                @click="$emit('update:modelValue', false)"
                class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                <span class="sr-only">Close</span>
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Modal Body -->
            <div class="px-6 py-4">
              <slot></slot>
            </div>

            <!-- Modal Footer -->
            <div v-if="$slots.footer" class="flex items-center justify-end space-x-3 border-t border-gray-200 px-6 py-4 bg-gray-50">
              <slot name="footer"></slot>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </Transition>
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
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
  preventBodyScroll()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  document.body.style.overflow = ''
})

// Watch for modelValue changes to handle body scroll
import { watch } from 'vue'
watch(() => props.modelValue, preventBodyScroll)
</script>

<style scoped>
/* Modal backdrop transition */
.modal-backdrop-enter-active,
.modal-backdrop-leave-active {
  transition: opacity 0.3s ease;
}

.modal-backdrop-enter-from,
.modal-backdrop-leave-to {
  opacity: 0;
}

/* Modal content transition */
.modal-content-enter-active,
.modal-content-leave-active {
  transition: all 0.3s ease;
}

.modal-content-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(-20px);
}

.modal-content-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(-20px);
}
</style>
