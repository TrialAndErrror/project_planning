from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()


class Project(models.Model):
    """Main project model that contains stages and tasks"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Project status
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Stage(models.Model):
    """Stage within a project that can contain tasks"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stages')
    order = models.PositiveIntegerField(default=0)  # For ordering stages within a project
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Stage status
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    class Meta:
        ordering = ['project', 'order', 'created_at']
        unique_together = ['project', 'order']
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Task(models.Model):
    """Task model that can belong to a project and optionally to a stage"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Task status
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Priority
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Time estimates (in 15-minute increments)
    estimated_hours = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Estimated time in hours"
    )
    estimated_minutes = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Additional minutes (0-59)"
    )
    
    # Actual time tracking
    actual_hours = models.PositiveIntegerField(default=0)
    actual_minutes = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['project', 'stage', 'priority', 'created_at']
    
    def __str__(self):
        stage_info = f" ({self.stage.name})" if self.stage else ""
        return f"{self.project.name}{stage_info} - {self.name}"
    
    @property
    def estimated_time_minutes(self):
        """Get total estimated time in minutes"""
        return (self.estimated_hours * 60) + self.estimated_minutes
    
    @property
    def actual_time_minutes(self):
        """Get total actual time in minutes"""
        return (self.actual_hours * 60) + self.actual_minutes
    
    @property
    def estimated_time_formatted(self):
        """Get formatted estimated time string"""
        if self.estimated_hours > 0:
            return f"{self.estimated_hours}h {self.estimated_minutes}m"
        return f"{self.estimated_minutes}m"
    
    @property
    def actual_time_formatted(self):
        """Get formatted actual time string"""
        if self.actual_hours > 0:
            return f"{self.actual_hours}h {self.actual_minutes}m"
        return f"{self.actual_minutes}m"


class TaskTimeline(models.Model):
    """Timeline tracking for tasks with due dates and completion dates"""
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='timeline')
    planned_start_date = models.DateTimeField(null=True, blank=True)
    planned_due_date = models.DateTimeField(null=True, blank=True)
    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_completion_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['planned_due_date', 'planned_start_date']
    
    def __str__(self):
        return f"Timeline for {self.task.name}"
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.planned_due_date and not self.actual_completion_date:
            return timezone.now() > self.planned_due_date
        return False
    
    @property
    def is_completed(self):
        """Check if task is completed"""
        return self.actual_completion_date is not None
    
    @property
    def is_started(self):
        """Check if task has been started"""
        return self.actual_start_date is not None


class TaskDependency(models.Model):
    """Model to track dependencies between tasks"""
    dependent_task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='dependencies'
    )
    prerequisite_task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='dependent_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['dependent_task', 'prerequisite_task']
        ordering = ['dependent_task', 'prerequisite_task']
    
    def __str__(self):
        return f"{self.dependent_task.name} depends on {self.prerequisite_task.name}"
    
    def clean(self):
        """Prevent circular dependencies"""
        if self.dependent_task == self.prerequisite_task:
            raise ValidationError("A task cannot depend on itself")
        
        # Check for circular dependencies
        if self._has_circular_dependency():
            raise ValidationError("Circular dependency detected")
    
    def _has_circular_dependency(self):
        """Check if this dependency would create a circular dependency"""
        visited = set()
        stack = [self.dependent_task]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            
            for dep in current.dependencies.all():
                if dep.prerequisite_task == self.prerequisite_task:
                    return True
                stack.append(dep.prerequisite_task)
        
        return False 