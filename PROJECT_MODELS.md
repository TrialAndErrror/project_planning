# Project Planning Models & API Documentation

## Overview

The project planning system consists of five main models that work together to provide comprehensive project management capabilities:

1. **Project** - The main container for all project-related data
2. **Stage** - Phases within a project that can contain tasks
3. **Task** - Individual work items that can belong to a project and optionally to a stage
4. **TaskTimeline** - Timeline tracking for tasks with due dates and completion dates
5. **TaskDependency** - Dependencies between tasks

## Model Relationships

```
Project (1) ←→ (N) Stage
Project (1) ←→ (N) Task
Stage (1) ←→ (N) Task
Task (1) ←→ (1) TaskTimeline
Task (N) ←→ (N) Task (via TaskDependency)
```

## Models

### Project

**Purpose**: Main container for project management

**Fields**:
- `name` (CharField) - Project name
- `description` (TextField) - Project description
- `owner` (ForeignKey to User) - Project owner
- `status` (CharField) - Project status (planning, active, on_hold, completed, cancelled)
- `created_at` (DateTimeField) - Creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

**Computed Fields**:
- `stage_count` - Number of stages in the project
- `task_count` - Number of tasks in the project
- `completed_task_count` - Number of completed tasks
- `progress_percentage` - Project completion percentage

### Stage

**Purpose**: Phases within a project that can contain tasks

**Fields**:
- `name` (CharField) - Stage name
- `description` (TextField) - Stage description
- `project` (ForeignKey to Project) - Parent project
- `owner` (ForeignKey to User) - Stage owner
- `order` (PositiveIntegerField) - Order within project
- `status` (CharField) - Stage status (not_started, in_progress, completed)
- `created_at` (DateTimeField) - Creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

**Computed Fields**:
- `task_count` - Number of tasks in this stage
- `completed_task_count` - Number of completed tasks in this stage

### Task

**Purpose**: Individual work items with time tracking and timeline management

**Fields**:
- `name` (CharField) - Task name
- `description` (TextField) - Task description
- `project` (ForeignKey to Project) - Required parent project
- `stage` (ForeignKey to Stage) - Optional parent stage
- `owner` (ForeignKey to User) - Task owner
- `status` (CharField) - Task status (not_started, in_progress, review, completed, blocked)
- `priority` (CharField) - Task priority (low, medium, high, urgent)
- `estimated_hours` (PositiveIntegerField) - Estimated time in hours
- `estimated_minutes` (PositiveIntegerField) - Additional estimated minutes (0-59, 15-min increments)
- `actual_hours` (PositiveIntegerField) - Actual time spent in hours
- `actual_minutes` (PositiveIntegerField) - Additional actual minutes (0-59, 15-min increments)
- `created_at` (DateTimeField) - Creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

**Computed Fields**:
- `estimated_time_minutes` - Total estimated time in minutes
- `actual_time_minutes` - Total actual time in minutes
- `estimated_time_formatted` - Formatted estimated time string (e.g., "2h 30m")
- `actual_time_formatted` - Formatted actual time string (e.g., "1h 45m")

### TaskTimeline

**Purpose**: Timeline tracking for tasks with due dates and completion dates

**Fields**:
- `task` (OneToOneField to Task) - Associated task
- `planned_start_date` (DateTimeField) - Planned start date
- `planned_due_date` (DateTimeField) - Planned due date
- `actual_start_date` (DateTimeField) - Actual start date
- `actual_completion_date` (DateTimeField) - Actual completion date
- `created_at` (DateTimeField) - Creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

**Computed Fields**:
- `is_overdue` - Whether the task is overdue
- `is_completed` - Whether the task is completed
- `is_started` - Whether the task has been started

### TaskDependency

**Purpose**: Dependencies between tasks to ensure proper execution order

**Fields**:
- `dependent_task` (ForeignKey to Task) - Task that depends on another
- `prerequisite_task` (ForeignKey to Task) - Task that must be completed first
- `created_at` (DateTimeField) - Creation timestamp

**Validation**:
- Tasks must belong to the same project
- A task cannot depend on itself
- Circular dependencies are prevented

## API Endpoints

### Projects

- `GET /api/projects/` - List all projects for the authenticated user
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}/` - Get project details with nested stages and tasks
- `PUT /api/projects/{id}/` - Update a project
- `DELETE /api/projects/{id}/` - Delete a project
- `GET /api/projects/{id}/timeline/` - Get timeline view of project tasks
- `GET /api/projects/{id}/statistics/` - Get project statistics

### Stages

- `GET /api/stages/` - List all stages for projects owned by the user
- `POST /api/stages/` - Create a new stage
- `GET /api/stages/{id}/` - Get stage details
- `PUT /api/stages/{id}/` - Update a stage
- `DELETE /api/stages/{id}/` - Delete a stage
- `POST /api/stages/{id}/reorder/` - Reorder stages within a project

### Tasks

- `GET /api/tasks/` - List all tasks for projects owned by the user
- `POST /api/tasks/` - Create a new task (with optional timeline)
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update a task
- `DELETE /api/tasks/{id}/` - Delete a task
- `POST /api/tasks/{id}/start/` - Mark task as started
- `POST /api/tasks/{id}/complete/` - Mark task as completed
- `POST /api/tasks/{id}/add_time/` - Add actual time to task
- `GET /api/tasks/overdue/` - Get overdue tasks
- `GET /api/tasks/upcoming/` - Get upcoming tasks (due in next 7 days)

### Task Timelines

- `GET /api/timelines/` - List all task timelines
- `POST /api/timelines/` - Create a new task timeline
- `GET /api/timelines/{id}/` - Get timeline details
- `PUT /api/timelines/{id}/` - Update a timeline
- `DELETE /api/timelines/{id}/` - Delete a timeline

### Task Dependencies

- `GET /api/dependencies/` - List all task dependencies
- `POST /api/dependencies/` - Create a new task dependency
- `GET /api/dependencies/{id}/` - Get dependency details
- `PUT /api/dependencies/{id}/` - Update a dependency
- `DELETE /api/dependencies/{id}/` - Delete a dependency

## Example Usage

### Creating a Project with Stages and Tasks

```bash
# 1. Create a project
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Website Redesign","description":"Redesign company website"}' \
  http://localhost:8000/api/projects/

# 2. Create stages
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Planning","project":1,"order":1}' \
  http://localhost:8000/api/stages/

curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Design","project":1,"order":2}' \
  http://localhost:8000/api/stages/

# 3. Create tasks with timeline
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Gather Requirements",
    "description":"Collect requirements from stakeholders",
    "project":1,
    "stage":1,
    "priority":"high",
    "estimated_hours":4,
    "estimated_minutes":30,
    "timeline":{
      "planned_start_date":"2025-09-01T09:00:00Z",
      "planned_due_date":"2025-09-03T17:00:00Z"
    }
  }' \
  http://localhost:8000/api/tasks/
```

### Time Tracking

```bash
# Add actual time to a task
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hours":2,"minutes":45}' \
  http://localhost:8000/api/tasks/1/add_time/
```

### Task Management

```bash
# Start a task
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/tasks/1/start/

# Complete a task
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/tasks/1/complete/
```

## Key Features

1. **15-Minute Time Increments**: All time estimates and actual time must be in 15-minute increments
2. **Automatic Timeline Creation**: Each task automatically gets a timeline record
3. **Progress Tracking**: Automatic calculation of project and stage progress
4. **Dependency Management**: Prevent circular dependencies and ensure proper task ordering
5. **Time Tracking**: Track estimated vs actual time for better project planning
6. **Status Management**: Comprehensive status tracking for projects, stages, and tasks
7. **Owner-Based Permissions**: Users can only access their own projects and tasks

## Validation Rules

1. **Time Increments**: Minutes must be in 15-minute increments (0, 15, 30, 45)
2. **Task Dependencies**: Tasks must belong to the same project
3. **Stage Order**: Stages have unique order within a project
4. **Required Fields**: Project is required for tasks, stage is optional
5. **Circular Dependencies**: Prevented through validation logic 