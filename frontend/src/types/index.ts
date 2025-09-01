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
  title: string
  description: string
  created_at: string
  updated_at: string
  owner: User
  stages: Stage[]
  stage_count?: number
  task_count?: number
  completed_task_count?: number
  progress_percentage?: number
}

export interface Stage {
  id: number
  title: string
  description: string
  order: number
  project: number
  tasks: Task[]
  created_at: string
  updated_at: string
  task_count?: number
  completed_task_count?: number
}

export interface Task {
  id: number
  title: string
  description: string
  status: 'todo' | 'in_progress' | 'done'
  priority: 'low' | 'medium' | 'high'
  stage: number
  assigned_to?: User
  due_date?: string
  created_at: string
  updated_at: string
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

export interface ApiResponse<T = any> {
  data: T
  status: number
  statusText: string
}

// Form types
export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  email: string
  password1: string
  password2: string
  username?: string
}

export interface ProjectForm {
  title: string
  description: string
}

export interface StageForm {
  title: string
  description: string
}

export interface TaskForm {
  title: string
  description: string
  status: 'todo' | 'in_progress' | 'done'
  priority: 'low' | 'medium' | 'high'
  stage: number
  assigned_to?: number
  due_date?: string
}

// Store types
export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

export interface ProjectState {
  projects: Project[]
  currentProject: Project | null
  loading: boolean
  error: string | null
}

// Router types
export interface RouteMeta extends Record<string, unknown> {
  requiresAuth?: boolean
  requiresGuest?: boolean
}
