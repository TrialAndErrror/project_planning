<template>
  <div class="project-detail">
    <div class="container-fluid py-4">
      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height: 300px;">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-5">
        <div class="alert alert-danger d-inline-block" role="alert">
          <i class="bi bi-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
        <div class="mt-3">
          <button @click="loadProject" class="btn btn-outline-primary">
            <i class="bi bi-arrow-clockwise me-2"></i>Try Again
          </button>
        </div>
      </div>

      <!-- Project Content -->
      <div v-else-if="project">
        <!-- Project Header -->
        <div class="card shadow-sm border-0 mb-4">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-start mb-4">
              <div class="flex-grow-1 me-3">
                <h1 class="h2 text-dark mb-2">{{ project.name }}</h1>
                <p class="text-muted mb-0">{{ project.description || 'No description' }}</p>
              </div>
              <div class="d-flex align-items-center gap-3">
                <span class="badge rounded-pill px-3 py-2" :class="statusClasses">
                  {{ getStatusLabel(project.status) }}
                </span>
                <button
                  @click="showEditModal = true"
                  class="btn btn-primary btn-sm"
                >
                  <i class="bi bi-pencil me-2"></i>Edit Project
                </button>
              </div>
            </div>

            <!-- Project Stats -->
            <div class="row g-3">
              <div class="col-6 col-md-3">
                <div class="card bg-light border-0 text-center">
                  <div class="card-body p-3">
                    <div class="h4 fw-bold text-primary mb-1">{{ project.stage_count }}</div>
                    <div class="small text-muted">Stages</div>
                  </div>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="card bg-light border-0 text-center">
                  <div class="card-body p-3">
                    <div class="h4 fw-bold text-success mb-1">{{ project.task_count }}</div>
                    <div class="small text-muted">Tasks</div>
                  </div>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="card bg-light border-0 text-center">
                  <div class="card-body p-3">
                    <div class="h4 fw-bold text-warning mb-1">{{ project.completed_task_count }}</div>
                    <div class="small text-muted">Completed</div>
                  </div>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="card bg-light border-0 text-center">
                  <div class="card-body p-3">
                    <div class="h4 fw-bold text-info mb-1">{{ project.progress_percentage }}%</div>
                    <div class="small text-muted">Progress</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tree View -->
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h2 class="h4 text-dark mb-0">Project Structure</h2>
              <div class="d-flex gap-2">
                <button
                  @click="showAddStageModal = true"
                  class="btn btn-success btn-sm"
                >
                  <i class="bi bi-plus-circle me-2"></i>Add Stage
                </button>
                <button
                  @click="showAddTaskModal = true"
                  class="btn btn-primary btn-sm"
                >
                  <i class="bi bi-plus-circle me-2"></i>Add Task
                </button>
              </div>
            </div>

            <!-- Stages and Tasks Tree -->
            <div class="space-y-3">
              <!-- Stages -->
              <div v-for="stage in project.stages" :key="stage.id" class="card border">
                <div class="card-header bg-light py-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center gap-3">
                      <i class="bi bi-folder text-muted"></i>
                      <span class="fw-semibold text-dark">{{ stage.name }}</span>
                      <span class="badge rounded-pill" :class="getStatusBadgeClasses(stage.status)">
                        {{ getStatusLabel(stage.status) }}
                      </span>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                      <small class="text-muted">{{ stage.task_count }} tasks</small>
                      <button
                        @click="editStage(stage)"
                        class="btn btn-outline-primary btn-sm"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button
                        @click="deleteStage(stage.id)"
                        class="btn btn-outline-danger btn-sm"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Tasks in this stage -->
                <div class="card-body pt-0">
                  <div v-for="task in getTasksForStage(stage.id)" :key="task.id" class="border-start border-2 border-light ps-3 ms-2 mb-3">
                    <div class="d-flex justify-content-between align-items-center py-2">
                      <div class="d-flex align-items-center gap-3">
                        <i class="bi bi-check2-square text-muted"></i>
                        <span class="text-dark">{{ task.name }}</span>
                        <span class="badge rounded-pill" :class="getPriorityBadgeClasses(task.priority)">
                          {{ task.priority }}
                        </span>
                        <span class="badge rounded-pill" :class="getStatusBadgeClasses(task.status)">
                          {{ getStatusLabel(task.status) }}
                        </span>
                      </div>
                      <div class="d-flex align-items-center gap-2">
                        <small class="text-muted">{{ task.estimated_time_formatted }}</small>
                        <button
                          v-if="task.status !== 'completed'"
                          @click="completeTask(task.id)"
                          class="btn btn-outline-success btn-sm"
                          title="Mark as complete"
                        >
                          <i class="bi bi-check-lg"></i>
                        </button>
                        <button
                          @click="editTask(task)"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button
                          @click="deleteTask(task.id)"
                          class="btn btn-outline-danger btn-sm"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Tasks without stage -->
              <div v-if="getTasksWithoutStage().length > 0" class="card border">
                <div class="card-header bg-light py-3">
                  <div class="d-flex align-items-center gap-3">
                    <i class="bi bi-list-task text-muted"></i>
                    <span class="fw-semibold text-dark">General Tasks</span>
                  </div>
                </div>
                <div class="card-body pt-0">
                  <div v-for="task in getTasksWithoutStage()" :key="task.id" class="border-start border-2 border-light ps-3 ms-2 mb-3">
                    <div class="d-flex justify-content-between align-items-center py-2">
                      <div class="d-flex align-items-center gap-3">
                        <i class="bi bi-check2-square text-muted"></i>
                        <span class="text-dark">{{ task.name }}</span>
                        <span class="badge rounded-pill" :class="getPriorityBadgeClasses(task.priority)">
                          {{ task.priority }}
                        </span>
                        <span class="badge rounded-pill" :class="getStatusBadgeClasses(task.status)">
                          {{ getStatusLabel(task.status) }}
                        </span>
                      </div>
                      <div class="d-flex align-items-center gap-2">
                        <small class="text-muted">{{ task.estimated_time_formatted }}</small>
                        <button
                          v-if="task.status !== 'completed'"
                          @click="completeTask(task.id)"
                          class="btn btn-outline-success btn-sm"
                          title="Mark as complete"
                        >
                          <i class="bi bi-check-lg"></i>
                        </button>
                        <button
                          @click="editTask(task)"
                          class="btn btn-outline-primary btn-sm"
                        >
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button
                          @click="deleteTask(task.id)"
                          class="btn btn-outline-danger btn-sm"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
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
    'bg-warning bg-opacity-10 text-warning': status === 'planning',
    'bg-success bg-opacity-10 text-success': status === 'active',
    'bg-warning bg-opacity-10 text-warning': status === 'on_hold',
    'bg-primary bg-opacity-10 text-primary': status === 'completed',
    'bg-danger bg-opacity-10 text-danger': status === 'cancelled'
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
    planning: 'bg-warning bg-opacity-10 text-warning',
    active: 'bg-success bg-opacity-10 text-success',
    on_hold: 'bg-warning bg-opacity-10 text-warning',
    completed: 'bg-primary bg-opacity-10 text-primary',
    cancelled: 'bg-danger bg-opacity-10 text-danger',
    not_started: 'bg-secondary bg-opacity-10 text-secondary',
    in_progress: 'bg-primary bg-opacity-10 text-primary',
    review: 'bg-info bg-opacity-10 text-info',
    blocked: 'bg-danger bg-opacity-10 text-danger'
  }
  return classes[status] || 'bg-secondary bg-opacity-10 text-secondary'
}

const getPriorityBadgeClasses = (priority) => {
  const classes = {
    low: 'bg-secondary bg-opacity-10 text-secondary',
    medium: 'bg-warning bg-opacity-10 text-warning',
    high: 'bg-warning bg-opacity-10 text-warning',
    urgent: 'bg-danger bg-opacity-10 text-danger'
  }
  return classes[priority] || 'bg-secondary bg-opacity-10 text-secondary'
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
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 0.75rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-1px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
  border-bottom: 1px solid #dee2e6;
}

.border-start {
  border-left: 2px solid #dee2e6 !important;
}

.space-y-3 > * + * {
  margin-top: 1rem;
}

@media (max-width: 767.98px) {
  .project-detail {
    padding: 0.5rem;
  }
  
  .card-body {
    padding: 1.5rem !important;
  }
  
  .d-flex.justify-content-between.align-items-start {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 1rem;
  }
  
  .btn {
    width: 100%;
  }
}
</style> 