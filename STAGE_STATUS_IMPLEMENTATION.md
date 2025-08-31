# Automatic Stage Status Implementation

## Overview
Implemented automatic stage status calculation based on the status of tasks within each stage, removing the need for manual status management.

## Status Calculation Rules

The stage status is automatically calculated using the following logic:

1. **No Tasks**: Stage status = "Not Started"
2. **All Tasks Not Started**: Stage status = "Not Started"
3. **At Least One Task In Progress or Further**: Stage status = "In Progress"
4. **All Tasks Completed**: Stage status = "Completed"

## Backend Changes

### 1. Stage Model (`backend/projects/models.py`)
- **Removed**: `status` field and `STATUS_CHOICES`
- **Added**: `calculated_status` property method that implements the status calculation logic

```python
@property
def calculated_status(self):
    """
    Calculate stage status based on the status of tasks within this stage.
    
    Rules:
    - If no tasks: "Not Started"
    - If all tasks are "Not Started": "Not Started" 
    - If at least one task is "In Progress" or further: "In Progress"
    - If all tasks are "Completed": "Completed"
    """
    tasks = self.tasks.all()
    
    if not tasks.exists():
        return 'not_started'
    
    # Get all task statuses
    task_statuses = list(tasks.values_list('status', flat=True))
    
    # If all tasks are completed
    if all(status == 'completed' for status in task_statuses):
        return 'completed'
    
    # If at least one task is in progress or further (not just not_started)
    if any(status in ['in_progress', 'review', 'completed', 'blocked'] for status in task_statuses):
        return 'in_progress'
    
    # If all tasks are not started
    if all(status == 'not_started' for status in task_statuses):
        return 'not_started'
    
    # Default fallback
    return 'in_progress'
```

### 2. Serializers (`backend/projects/serializers.py`)
- **StageSerializer**: Updated to use `calculated_status` instead of stored status
- **StageCreateSerializer**: Removed status field from creation form

```python
class StageSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()  # Use calculated status
    
    def get_status(self, obj):
        """Get the calculated status based on tasks"""
        return obj.calculated_status

class StageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['name', 'description', 'project', 'order']  # Removed status
```

### 3. Database Migration (`backend/projects/migrations/0002_remove_stage_status_field.py`)
- **Created**: Migration to remove the `status` field from the Stage model
- **Applied**: Successfully migrated the database

```python
operations = [
    migrations.RemoveField(
        model_name='stage',
        name='status',
    ),
]
```

### 4. Admin Configuration (`backend/projects/admin.py`)
- **Updated**: StageAdmin to use calculated status instead of stored status field
- **Added**: Custom method to display calculated status in Django admin

```python
@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'owner', 'order', 'calculated_status', 'created_at']
    list_filter = ['project', 'created_at', 'owner']  # Removed status filter
    readonly_fields = ['created_at', 'updated_at', 'calculated_status']
    
    def calculated_status(self, obj):
        """Display the calculated status in the admin"""
        return obj.calculated_status
    calculated_status.short_description = 'Status'
```

### 5. Sample Data (`backend/fixtures/sample_data.json`)
- **Updated**: Removed all `status` fields from stage entries
- **Result**: Stage statuses will now be calculated automatically based on task statuses

## Frontend Changes

### 1. AddStageModal (`frontend/src/components/AddStageModal.vue`)
- **Removed**: Status field from form data
- **Updated**: Form validation and submission logic

```javascript
const form = reactive({
  name: '',
  description: '',
  order: '',
  project: props.projectId  // Removed status field
})
```

### 2. EditStageModal (`frontend/src/components/EditStageModal.vue`)
- **Removed**: Status field from template and form data
- **Updated**: Form initialization and submission logic

```javascript
const form = reactive({
  name: '',
  description: '',
  order: 0  // Removed status field
})
```

## Testing

### Test Script (`backend/test_stage_status.py`)
Created and ran comprehensive tests to verify the status calculation logic:

1. **No Tasks**: ✅ Returns "not_started"
2. **All Tasks Not Started**: ✅ Returns "not_started"
3. **One Task In Progress**: ✅ Returns "in_progress"
4. **All Tasks Completed**: ✅ Returns "completed"
5. **Mixed Statuses**: ✅ Returns "in_progress"

## Benefits

1. **Automatic Updates**: Stage status automatically updates when task statuses change
2. **Consistency**: Eliminates manual status management errors
3. **Real-time Accuracy**: Status always reflects the current state of tasks
4. **Simplified UI**: Removes unnecessary status selection from stage forms
5. **Data Integrity**: Prevents inconsistent status states

## Usage

The stage status is now automatically calculated and displayed throughout the application:

- **API Responses**: Stage serializers return calculated status
- **Frontend Display**: Stage cards and lists show calculated status
- **Real-time Updates**: Status changes when tasks are updated
- **No Manual Input**: Users cannot manually set stage status

## Migration Notes

- Existing stage data will have their status calculated automatically
- No data loss - status is derived from task relationships
- Backward compatible - API responses still include status field
- Frontend components automatically adapt to calculated values
