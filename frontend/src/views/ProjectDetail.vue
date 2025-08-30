<template>
  <div class="project-detail">
    <div class="container mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <div class="text-red-600 text-lg mb-4">{{ error }}</div>
        <button @click="loadProject" class="text-blue-600 hover:text-blue-800">
          Try Again
        </button>
      </div>

      <!-- Project Content -->
      <div v-else-if="project" class="space-y-6">
        <!-- Project Header -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">{{ project.name }}</h1>
              <p class="text-gray-600 mt-2">{{ project.description || 'No description' }}</p>
            </div>
            <div class="flex items-center space-x-4">
              <span class="px-3 py-1 rounded-full text-sm font-medium" :class="statusClasses">
                {{ getStatusLabel(project.status) }}
              </span>
              <button
                @click="showEditModal = true"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Edit Project
              </button>
            </div>
          </div>

          <!-- Project Stats -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-gray-900">{{ project.stage_count }}</div>
              <div class="text-sm text-gray-600">Stages</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-gray-900">{{ project.task_count }}</div>
              <div class="text-sm text-gray-600">Tasks</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-gray-900">{{ project.completed_task_count }}</div>
              <div class="text-sm text-gray-600">Completed</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-gray-900">{{ project.progress_percentage }}%</div>
              <div class="text-sm text-gray-600">Progress</div>
            </div>
          </div>
        </div>

        <!-- Tree View -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold text-gray-900">Project Structure</h2>
            <div class="flex space-x-2">
              <button
                @click="showAddStageModal = true"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                + Add Stage
              </button>
              <button
                @click="showAddTaskModal = true"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                + Add Task
              </button>
            </div>
          </div>

          <!-- Stages and Tasks Tree -->
          <div class="space-y-4">
            <!-- Stages -->
            <div v-for="stage in project.stages" :key="stage.id" class="border border-gray-200 rounded-lg">
              <div class="bg-gray-50 px-4 py-3 flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                  </svg>
                  <span class="font-medium text-gray-900">{{ stage.name }}</span>
                  <span class="px-2 py-1 text-xs rounded-full" :class="getStatusBadgeClasses(stage.status)">
                    {{ getStatusLabel(stage.status) }}
                  </span>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-sm text-gray-500">{{ stage.task_count }} tasks</span>
                  <button
                    @click="editStage(stage)"
                    class="text-blue-600 hover:text-blue-800"
                  >
                    Edit
                  </button>
                  <button
                    @click="deleteStage(stage.id)"
                    class="text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>

              <!-- Tasks in this stage -->
              <div class="p-4 space-y-2">
                <div v-for="task in getTasksForStage(stage.id)" :key="task.id" class="ml-6 border-l-2 border-gray-200 pl-4">
                  <div class="flex items-center justify-between py-2">
                    <div class="flex items-center space-x-3">
                      <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                      </svg>
                      <span class="text-gray-900">{{ task.name }}</span>
                      <span class="px-2 py-1 text-xs rounded-full" :class="getPriorityBadgeClasses(task.priority)">
                        {{ task.priority }}
                      </span>
                      <span class="px-2 py-1 text-xs rounded-full" :class="getStatusBadgeClasses(task.status)">
                        {{ getStatusLabel(task.status) }}
                      </span>
                    </div>
                    <div class="flex items-center space-x-2">
                      <span class="text-sm text-gray-500">{{ task.estimated_time_formatted }}</span>
                      <button
                        v-if="task.status !== 'completed'"
                        @click="completeTask(task.id)"
                        class="text-green-600 hover:text-green-800"
                        title="Mark as complete"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                      </button>
                      <button
                        @click="editTask(task)"
                        class="text-blue-600 hover:text-blue-800"
                      >
                        Edit
                      </button>
                      <button
                        @click="deleteTask(task.id)"
                        class="text-red-600 hover:text-red-800"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

                          <!-- Tasks without stage -->
              <div v-if="getTasksWithoutStage().length > 0" class="border border-gray-200 rounded-lg">
                <div class="bg-gray-50 px-4 py-3">
                  <div class="flex items-center space-x-3">
                    <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                    <span class="font-medium text-gray-900">General Tasks</span>
                  </div>
                </div>
                <div class="p-4 space-y-2">
                  <div v-for="task in getTasksWithoutStage()" :key="task.id" class="ml-6 border-l-2 border-gray-200 pl-4">
                    <div class="flex items-center justify-between py-2">
                      <div class="flex items-center space-x-3">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                        </svg>
                        <span class="text-gray-900">{{ task.name }}</span>
                        <span class="px-2 py-1 text-xs rounded-full" :class="getPriorityBadgeClasses(task.priority)">
                          {{ task.priority }}
                        </span>
                        <span class="px-2 py-1 text-xs rounded-full" :class="getStatusBadgeClasses(task.status)">
                          {{ getStatusLabel(task.status) }}
                        </span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <span class="text-sm text-gray-500">{{ task.estimated_time_formatted }}</span>
                        <button
                          v-if="task.status !== 'completed'"
                          @click="completeTask(task.id)"
                          class="text-green-600 hover:text-green-800"
                          title="Mark as complete"
                        >
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                          </svg>
                        </button>
                        <button
                          @click="editTask(task)"
                          class="text-blue-600 hover:text-blue-800"
                        >
                          Edit
                        </button>
                        <button
                          @click="deleteTask(task.id)"
                          class="text-red-600 hover:text-red-800"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
          </div>
        </div>
      </div>

      <!-- Edit Project Modal -->
      <EditProjectModal
        v-if="showEditModal"
        :project="project"
        @close="showEditModal = false"
        @saved="handleProjectUpdated"
      />

      <!-- Add Stage Modal -->
      <AddStageModal
        v-if="showAddStageModal"
        :project-id="projectId"
        @close="showAddStageModal = false"
        @saved="handleStageAdded"
      />

      <!-- Add Task Modal -->
      <AddTaskModal
        v-if="showAddTaskModal"
        :project-id="projectId"
        :stages="project?.stages || []"
        @close="showAddTaskModal = false"
        @saved="handleTaskAdded"
      />

      <!-- Edit Stage Modal -->
      <EditStageModal
        v-if="showEditStageModal"
        :stage="editingStage"
        @close="showEditStageModal = false"
        @saved="handleStageUpdated"
      />

      <!-- Edit Task Modal -->
      <EditTaskModal
        v-if="showEditTaskModal"
        :task="editingTask"
        :stages="project?.stages || []"
        @close="showEditTaskModal = false"
        @saved="handleTaskUpdated"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from '../stores/project'
import EditProjectModal from '../components/EditProjectModal.vue'
import AddStageModal from '../components/AddStageModal.vue'
import AddTaskModal from '../components/AddTaskModal.vue'
import EditStageModal from '../components/EditStageModal.vue'
import EditTaskModal from '../components/EditTaskModal.vue'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

const projectId = computed(() => route.params.id)
const project = computed(() => projectStore.currentProject)
const loading = computed(() => projectStore.loading)
const error = computed(() => projectStore.error)

// Modal states
const showEditModal = ref(false)
const showAddStageModal = ref(false)
const showAddTaskModal = ref(false)
const showEditStageModal = ref(false)
const showEditTaskModal = ref(false)

// Editing states
const editingStage = ref(null)
const editingTask = ref(null)

// Status classes
const statusClasses = computed(() => {
  if (!project.value) return ''
  const status = project.value.status
  return {
    'bg-yellow-100 text-yellow-800': status === 'planning',
    'bg-green-100 text-green-800': status === 'active',
    'bg-orange-100 text-orange-800': status === 'on_hold',
    'bg-blue-100 text-blue-800': status === 'completed',
    'bg-red-100 text-red-800': status === 'cancelled'
  }
})

// Load project data
const loadProject = async () => {
  const result = await projectStore.fetchProject(projectId.value)
  if (!result.success) {
    router.push('/projects')
  }
}

// Helper functions
const getStatusLabel = (status) => {
  const labels = {
    planning: 'Planning',
    active: 'Active',
    on_hold: 'On Hold',
    completed: 'Completed',
    cancelled: 'Cancelled',
    not_started: 'Not Started',
    in_progress: 'In Progress',
    review: 'In Review',
    blocked: 'Blocked'
  }
  return labels[status] || status
}

const getStatusBadgeClasses = (status) => {
  const classes = {
    planning: 'bg-yellow-100 text-yellow-800',
    active: 'bg-green-100 text-green-800',
    on_hold: 'bg-orange-100 text-orange-800',
    completed: 'bg-blue-100 text-blue-800',
    cancelled: 'bg-red-100 text-red-800',
    not_started: 'bg-gray-100 text-gray-800',
    in_progress: 'bg-blue-100 text-blue-800',
    review: 'bg-purple-100 text-purple-800',
    blocked: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPriorityBadgeClasses = (priority) => {
  const classes = {
    low: 'bg-gray-100 text-gray-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    urgent: 'bg-red-100 text-red-800'
  }
  return classes[priority] || 'bg-gray-100 text-gray-800'
}

const getTasksForStage = (stageId) => {
  if (!project.value) return []
  return project.value.tasks.filter(task => task.stage === stageId)
}

const getTasksWithoutStage = () => {
  if (!project.value) return []
  return project.value.tasks.filter(task => !task.stage)
}

// Event handlers
const handleProjectUpdated = () => {
  showEditModal.value = false
  loadProject()
}

const handleStageAdded = () => {
  showAddStageModal.value = false
  loadProject()
}

const handleTaskAdded = () => {
  showAddTaskModal.value = false
  loadProject()
}

const handleStageUpdated = () => {
  showEditStageModal.value = false
  editingStage.value = null
  loadProject()
}

const handleTaskUpdated = () => {
  showEditTaskModal.value = false
  editingTask.value = null
  loadProject()
}

const editStage = (stage) => {
  editingStage.value = stage
  showEditStageModal.value = true
}

const editTask = (task) => {
  editingTask.value = task
  showEditTaskModal.value = true
}

const deleteStage = async (stageId) => {
  if (confirm('Are you sure you want to delete this stage? This will also delete all tasks in this stage.')) {
    const result = await projectStore.deleteStage(stageId)
    if (result.success) {
      loadProject()
    }
  }
}

const deleteTask = async (taskId) => {
  if (confirm('Are you sure you want to delete this task?')) {
    const result = await projectStore.deleteTask(taskId)
    if (result.success) {
      loadProject()
    }
  }
}

const completeTask = async (taskId) => {
  const result = await projectStore.completeTask(taskId)
  if (result.success) {
    loadProject()
  } else {
    alert('Failed to complete task. Please try again.')
  }
}

// Load project on mount
onMounted(() => {
  loadProject()
})
</script>

<style scoped>
.project-detail {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style> 