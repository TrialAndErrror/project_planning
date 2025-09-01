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
        <div class="card shadow-sm border-0 mb-4 project-header-card">
          <div class="card-body">
            <div class="row mb-4">
              <div
                  class="col-12 col-lg-6 d-flex justify-content-between align-items-lg-start align-items-center flex-lg-column justify-content-lg-start">
                <h1 class="h2 text-dark mb-2">{{ project.name }}</h1>
                <p class="text-muted mb-0">{{ project.description || 'No description' }}</p>
              </div>
              <div class="col-12 col-lg-6 d-flex justify-content-center justify-content-lg-end align-items-center">
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
        <div class="card project-card shadow-sm border-0">
          <div class="card-body row">
            <div class="col-12 col-lg-6 d-flex justify-content-center justify-content-lg-start align-items-center my-2">
              <h2 class="h4 text-dark mb-0">Project Structure</h2>
            </div>
            <div class="col-12 col-lg-6 d-flex justify-content-center justify-content-lg-end align-items-center gap-2 px-4 my-2">
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

            <!-- Stages and Tasks Tree -->
            <div class="space-y-3" style="gap: 1rem;">
              <!-- Stages -->
              <div v-for="stage in project.stages" :key="stage.id" class="card border">
                <div
                    class="card-header bg-light py-3 stage-header"
                    @click="toggleStage(stage.id)"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="col-12 col-lg-6 d-flex align-items-center justify-content-between">
                      <div class="d-flex gap-3">
                        <i class="bi" :class="isStageExpanded(stage.id) ? 'bi-folder2-open' : 'bi-folder'"></i>
                        <span class="fw-semibold text-dark">{{ stage.name }}</span>
                      </div>
                      <div class="d-flex gap-3">
                      <span class="badge rounded-pill" :class="getStatusBadgeClasses(stage.status)">
                        {{ getStatusLabel(stage.status) }}
                      </span>
                      </div>
                    </div>
                    <div class="col-lg-6 d-none d-lg-flex align-items-center gap-2">
                      <small class="text-muted">{{ stage.task_count }} tasks</small>
                      <button
                          @click.stop="editStage(stage)"
                          class="btn btn-outline-primary btn-sm"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button
                          @click.stop="deleteStage(stage.id)"
                          class="btn btn-outline-danger btn-sm"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Tasks in this stage -->
                <div v-show="isStageExpanded(stage.id)" class="card-body pt-0">
                  <div v-for="task in getTasksForStage(stage.id)" :key="task.id" class="task-item">
                    <!-- Task Header -->
                    <div
                        class="d-flex justify-content-between align-items-center py-lg-2 task-header"
                        @click="toggleTask(task.id)"
                    >
                      <div class="d-flex gap-3">
                        <i class="bi bi-check2-square text-muted"></i>
                        <span class="text-dark">{{ task.name }}</span>
                      </div>
                      <div class="d-flex gap-3">
                          <span class="badge rounded-pill" :class="getPriorityBadgeClasses(task.priority)">
                          {{ task.priority }}
                        </span>
                        <span class="badge rounded-pill" :class="getStatusBadgeClasses(task.status)">
                          {{ getStatusLabel(task.status) }}
                        </span>
                        <small class="text-muted">{{ task.estimated_time_formatted }}</small>
                        <i class="bi" :class="isTaskExpanded(task.id) ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                      </div>
                    </div>

                    <!-- Task Details (Expandable) -->
                    <div v-show="isTaskExpanded(task.id)" class="mt-lg-3 task-details">
                      <!-- Task Description -->
                      <div v-if="task.description" class="mb-3">
                        <p class="text-muted mb-0">{{ task.description }}</p>
                      </div>

                      <!-- Task Action Buttons -->
                      <div class="d-flex gap-2 mt-3">
                        <button
                            v-if="task.status !== 'completed'"
                            @click="completeTask(task.id)"
                            class="btn btn-success btn-sm"
                        >
                          <i class="bi bi-check-lg me-1"></i>Completed
                        </button>
                        <button
                            @click="editTask(task)"
                            class="btn btn-primary btn-sm"
                        >
                          <i class="bi bi-pencil me-1"></i>Edit
                        </button>
                        <button
                            @click="deleteTask(task.id)"
                            class="btn btn-danger btn-sm"
                        >
                          <i class="bi bi-trash me-1"></i>Delete
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Tasks without stage (General Tasks) -->
              <div v-if="getTasksWithoutStage().length > 0" class="card project-card border">
                <div
                    class="card-header bg-light py-3 stage-header"
                    @click="toggleStage(0)"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center gap-3">
                      <i class="bi" :class="isStageExpanded(0) ? 'bi-list-task' : 'bi-list'"></i>
                      <span class="fw-semibold text-dark">General Tasks</span>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                      <small class="text-muted">{{ getTasksWithoutStage().length }} tasks</small>
                      <i class="bi" :class="isStageExpanded(0) ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                    </div>
                  </div>
                </div>
                <div v-show="isStageExpanded(0)" class="card-body pt-0">
                  <div v-for="task in getTasksWithoutStage()" :key="task.id" class="task-item">
                    <!-- Task Header -->
                    <div
                        class="d-flex justify-content-between align-items-center py-2 task-header"
                        @click="toggleTask(task.id)"
                    >
                      <i class="bi bi-check2-square text-muted"></i>
                      <span class="text-dark">{{ task.name }}</span>
                      <span class="badge rounded-pill" :class="getPriorityBadgeClasses(task.priority)">
                          {{ task.priority }}
                        </span>
                      <span class="badge rounded-pill" :class="getStatusBadgeClasses(task.status)">
                          {{ getStatusLabel(task.status) }}
                        </span>
                      <small class="text-muted">{{ task.estimated_time_formatted }}</small>
                      <i class="bi" :class="isTaskExpanded(task.id) ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                    </div>

                    <!-- Task Details (Expandable) -->
                    <div v-show="isTaskExpanded(task.id)" class="mt-lg-3 task-details">
                      <!-- Task Description -->
                      <div v-if="task.description" class="mb-3">
                        <p class="text-muted mb-0">{{ task.description }}</p>
                      </div>

                      <!-- Task Action Buttons -->
                      <div class="d-flex gap-2 mt-3 justify-content-end">
                        <button
                            v-if="task.status !== 'completed'"
                            @click="completeTask(task.id)"
                            class="btn btn-success btn-sm me-auto"
                        >
                          <i class="bi bi-check-lg me-1"></i>Completed
                        </button>
                        <button
                            @click="editTask(task)"
                            class="btn btn-primary btn-sm"
                        >
                          <i class="bi bi-pencil me-1"></i>Edit
                        </button>
                        <button
                            @click="deleteTask(task.id)"
                            class="btn btn-danger btn-sm"
                        >
                          <i class="bi bi-trash me-1"></i>Delete
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
          v-model="showEditModal"
          :project="project"
          @saved="handleProjectUpdated"
      />

      <!-- Add Stage Modal -->
      <AddStageModal
          v-model="showAddStageModal"
          :project-id="projectId"
          @saved="handleStageAdded"
      />

      <!-- Add Task Modal -->
      <AddTaskModal
          v-model="showAddTaskModal"
          :project-id="projectId"
          :stages="project?.stages || []"
          @saved="handleTaskAdded"
      />

      <!-- Edit Stage Modal -->
      <EditStageModal
          v-model="showEditStageModal"
          :stage="editingStage"
          @saved="handleStageUpdated"
      />

      <!-- Edit Task Modal -->
      <EditTaskModal
          v-model="showEditTaskModal"
          :task="editingTask"
          :stages="project?.stages || []"
          @saved="handleTaskUpdated"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useProjectStore} from '@/stores/project'
import EditProjectModal from '../components/EditProjectModal.vue'
import AddStageModal from '../components/AddStageModal.vue'
import AddTaskModal from '../components/AddTaskModal.vue'
import EditStageModal from '../components/EditStageModal.vue'
import EditTaskModal from '../components/EditTaskModal.vue'
import {Stage, Task} from "@/types";

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
const editingStage = ref({} as Stage)
const editingTask = ref({} as Task)


// Load project data
const loadProject = async () => {
  const result = await projectStore.fetchProject(projectId.value)
  if (!result.success) {
    router.push('/projects')
  }
}

// Helper functions - now using store functions
const getStatusLabel = projectStore.getStatusLabel
const getStatusBadgeClasses = projectStore.getStatusBadgeClasses
const getPriorityBadgeClasses = projectStore.getPriorityBadgeClasses
const getTasksForStage = projectStore.getTasksForStage
const getTasksWithoutStage = projectStore.getTasksWithoutStage

// Toggle methods - now using store functions
const toggleStage = projectStore.toggleStage
const toggleTask = projectStore.toggleTask
const isStageExpanded = projectStore.isStageExpanded
const isTaskExpanded = projectStore.isTaskExpanded

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
  editingStage.value = {} as Stage
  loadProject()
}

const handleTaskUpdated = () => {
  showEditTaskModal.value = false
  editingTask.value = {} as Task
  loadProject()
}

const editStage = (stage: Stage) => {
  editingStage.value = stage
  showEditStageModal.value = true
}

const editTask = (task: Task) => {
  editingTask.value = task
  showEditTaskModal.value = true
}

const deleteStage = async (stageId: number) => {
  if (confirm('Are you sure you want to delete this stage? This will also delete all tasks in this stage.')) {
    const result = await projectStore.deleteStage(stageId)
    if (result.success) {
      loadProject()
    }
  }
}

const deleteTask = async (taskId: number) => {
  if (confirm('Are you sure you want to delete this task?')) {
    const result = await projectStore.deleteTask(taskId)
    if (result.success) {
      loadProject()
    }
  }
}

const completeTask = async (taskId: number) => {
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
  transition: background-color 0.2s ease-in-out;
}

.card-header:hover {
  background-color: #e9ecef !important;
}

.space-y-3 {
  padding: 1.25rem;
}

.space-y-3 > * + * {
  margin-top: 1rem;
}

/* Task expansion animations */
.task-details {
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}

.task-details-enter-active,
.task-details-leave-active {
  transition: all 0.3s ease-in-out;
}

.task-details-enter-from,
.task-details-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Button hover effects */
.btn-sm {
  transition: all 0.2s ease-in-out;
}

.btn-sm:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

/* Stage header cursor and hover effects */
.stage-header {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.stage-header:hover {
  background-color: #e9ecef !important;
}

/* Task item styling */
.task-item {
  transition: all 0.2s ease-in-out;
  border-radius: 0.5rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  margin-left: 0.5rem;
  border-left: 2px solid transparent;
}

.task-item:hover {
  background-color: #f8f9fa;
  transform: translateX(2px);
  border-left-color: #dee2e6;
  padding-left: 1rem;
}

/* Task header styling */
.task-header {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  border-radius: 0.5rem;
  padding: 0.5rem;
  margin: -0.5rem;
}

.project-header-card .card-body {
  padding: 1.25rem;
}

@media (max-width: 900px) {
  .project-detail {
    padding: 0.25rem;
  }

  .card.project-card .card-body {
    padding: 0;
  }

  .btn {
    width: 100%;
  }

  .d-flex.gap-2 .btn {
    width: 100%;
  }
}

/* Status and Priority Badge Base Styles */


</style> 