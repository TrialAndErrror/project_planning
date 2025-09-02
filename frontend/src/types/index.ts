// User types
export interface User {
  id: number
  email: string
  username: string
  first_name?: string
  last_name?: string
  date_joined: string
}

// Project types
export interface Project {
  id: number
  name: string
  description: string
  created_at: string
  updated_at: string
  owner: User
  stages: Stage[]
  tasks?: Task[]
  stage_count?: number
  task_count?: number
  completed_task_count?: number
  progress_percentage?: number
}

export interface Stage {
  id: number
  name: string
  description: string
  order: number
  project: number
  tasks: Task[]
  created_at: string
  updated_at: string
  task_count?: number
  completed_task_count?: number
  status?: string
}

export interface Task {
  id: number
  name: string
  description: string
  status: 'not_started' | 'in_progress' | 'review' | 'completed' | 'blocked'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  stage?: number
  assigned_to?: User
  due_date?: string
  created_at: string
  updated_at: string
  // Additional fields from backend
  estimated_hours?: number
  estimated_minutes?: number
  estimated_time_formatted?: string
  actual_hours?: number
  actual_minutes?: number
  actual_time_formatted?: string
  project?: number
  project_name?: string
  stage_name?: string
  owner?: User
}

// API Response types
export interface LoginResponse {
  key: string
  user: User
}

export interface RegisterResponse {
  detail?: string
  email?: string[]
  password1?: string[]
  password2?: string[]
  username?: string[]
}

export interface AuthStatusResponse {
  authenticated: boolean
  user?: User
}

export interface ProjectForm {
  name: string
  description: string
}

export interface StageForm {
  name: string
  description: string
}

export interface TaskForm {
  name: string
  description: string
  status: 'not_started' | 'in_progress' | 'review' | 'completed' | 'blocked'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  stage?: number
  assigned_to?: number
  due_date?: string
}

