from django.contrib import admin
from .models import Project, Stage, Task, TaskTimeline, TaskDependency


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'owner']
    search_fields = ['name', 'description', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'owner', 'order', 'calculated_status', 'created_at']
    list_filter = ['project', 'created_at', 'owner']
    search_fields = ['name', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at', 'calculated_status']
    ordering = ['project', 'order']
    
    def calculated_status(self, obj):
        """Display the calculated status in the admin"""
        return obj.calculated_status
    calculated_status.short_description = 'Status'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'project', 'stage', 'owner', 'status', 'priority',
        'estimated_time_formatted', 'actual_time_formatted', 'created_at'
    ]
    list_filter = ['status', 'priority', 'project', 'stage', 'created_at', 'owner']
    search_fields = ['name', 'description', 'project__name', 'stage__name']
    readonly_fields = ['created_at', 'updated_at', 'estimated_time_formatted', 'actual_time_formatted']
    ordering = ['project', 'stage', 'priority', 'created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'project', 'stage', 'owner')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Time Tracking', {
            'fields': ('estimated_hours', 'estimated_minutes', 'actual_hours', 'actual_minutes'),
            'description': 'Time estimates and actual time spent (minutes must be in 15-minute increments)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaskTimeline)
class TaskTimelineAdmin(admin.ModelAdmin):
    list_display = [
        'task', 'planned_start_date', 'planned_due_date',
        'actual_start_date', 'actual_completion_date', 'is_overdue', 'is_completed'
    ]
    list_filter = ['planned_due_date', 'actual_completion_date']
    search_fields = ['task__name', 'task__project__name']
    readonly_fields = ['created_at', 'updated_at', 'is_overdue', 'is_completed', 'is_started']
    ordering = ['planned_due_date']


@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ['dependent_task', 'prerequisite_task', 'created_at']
    list_filter = ['created_at']
    search_fields = [
        'dependent_task__name', 'prerequisite_task__name',
        'dependent_task__project__name', 'prerequisite_task__project__name'
    ]
    readonly_fields = ['created_at']
    ordering = ['dependent_task', 'prerequisite_task'] 