from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models
from .models import Project, Stage, Task, TaskTimeline, TaskDependency

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Simple user serializer for nested relationships"""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']


class TaskTimelineSerializer(serializers.ModelSerializer):
    """Serializer for task timeline"""
    is_overdue = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    is_started = serializers.ReadOnlyField()
    
    class Meta:
        model = TaskTimeline
        fields = [
            'id', 'planned_start_date', 'planned_due_date', 
            'actual_start_date', 'actual_completion_date',
            'is_overdue', 'is_completed', 'is_started',
            'created_at', 'updated_at'
        ]


class TaskDependencySerializer(serializers.ModelSerializer):
    """Serializer for task dependencies"""
    prerequisite_task_name = serializers.CharField(source='prerequisite_task.name', read_only=True)
    dependent_task_name = serializers.CharField(source='dependent_task.name', read_only=True)
    
    class Meta:
        model = TaskDependency
        fields = [
            'id', 'dependent_task', 'prerequisite_task',
            'dependent_task_name', 'prerequisite_task_name',
            'created_at'
        ]


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks"""
    owner = UserSerializer(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    stage_name = serializers.CharField(source='stage.name', read_only=True)
    estimated_time_formatted = serializers.ReadOnlyField()
    actual_time_formatted = serializers.ReadOnlyField()
    timeline = TaskTimelineSerializer(read_only=True)
    dependencies = TaskDependencySerializer(many=True, read_only=True)
    dependent_tasks = TaskDependencySerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'project', 'project_name',
            'stage', 'stage_name', 'owner', 'status', 'priority',
            'estimated_hours', 'estimated_minutes', 'estimated_time_formatted',
            'actual_hours', 'actual_minutes', 'actual_time_formatted',
            'timeline', 'dependencies', 'dependent_tasks',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def validate_estimated_minutes(self, value):
        """Validate that minutes are in 15-minute increments"""
        if value % 15 != 0:
            raise serializers.ValidationError("Minutes must be in 15-minute increments")
        return value
    
    def validate_actual_minutes(self, value):
        """Validate that minutes are in 15-minute increments"""
        if value % 15 != 0:
            raise serializers.ValidationError("Minutes must be in 15-minute increments")
        return value


class StageSerializer(serializers.ModelSerializer):
    """Serializer for stages"""
    owner = UserSerializer(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    completed_task_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()  # Use calculated status
    
    class Meta:
        model = Stage
        fields = [
            'id', 'name', 'description', 'project', 'project_name',
            'owner', 'order', 'status', 'tasks', 'task_count',
            'completed_task_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def get_status(self, obj):
        """Get the calculated status based on tasks"""
        return obj.calculated_status
    
    def get_task_count(self, obj):
        """Get total number of tasks in this stage"""
        return obj.tasks.count()
    
    def get_completed_task_count(self, obj):
        """Get number of completed tasks in this stage"""
        return obj.tasks.filter(status='completed').count()


class StageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating stages"""
    order = serializers.IntegerField(required=False, default=0)
    
    class Meta:
        model = Stage
        fields = ['name', 'description', 'project', 'order']
    
    def validate_order(self, value):
        """Validate order field"""
        if value is None or value == '':
            return 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    
    def create(self, validated_data):
        """Create stage with proper order handling"""
        project = validated_data['project']
        order = validated_data.get('order', 0)
        
        # If order is 0 or not specified, set it to the next available order
        if order == 0:
            max_order = Stage.objects.filter(project=project).aggregate(
                models.Max('order')
            )['order__max'] or 0
            validated_data['order'] = max_order + 1
        
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for projects"""
    owner = UserSerializer(read_only=True)
    stages = StageSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    stage_count = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()
    completed_task_count = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    total_estimated_hours = serializers.SerializerMethodField()
    total_estimated_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'owner', 'status',
            'stages', 'tasks', 'stage_count', 'task_count',
            'completed_task_count', 'progress_percentage',
            'total_estimated_hours', 'total_estimated_minutes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def get_stage_count(self, obj):
        """Get total number of stages in this project"""
        return obj.stages.count()
    
    def get_task_count(self, obj):
        """Get total number of tasks in this project"""
        return obj.tasks.count()
    
    def get_completed_task_count(self, obj):
        """Get number of completed tasks in this project"""
        return obj.tasks.filter(status='completed').count()
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage based on completed tasks"""
        total_tasks = obj.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = obj.tasks.filter(status='completed').count()
        return round((completed_tasks / total_tasks) * 100, 1)
    
    def get_total_estimated_hours(self, obj):
        """Calculate total estimated hours for incomplete tasks in this project"""
        # Only include incomplete tasks from incomplete projects
        if obj.status == 'completed':
            return 0
        
        total_hours = obj.tasks.filter(status__in=['not_started', 'in_progress', 'review', 'blocked']).aggregate(
            total=models.Sum('estimated_hours')
        )['total'] or 0
        return total_hours
    
    def get_total_estimated_minutes(self, obj):
        """Calculate total estimated minutes for incomplete tasks in this project"""
        # Only include incomplete tasks from incomplete projects
        if obj.status == 'completed':
            return 0
        
        total_minutes = obj.tasks.filter(status__in=['not_started', 'in_progress', 'review', 'blocked']).aggregate(
            total=models.Sum('estimated_minutes')
        )['total'] or 0
        return total_minutes


class ProjectDetailSerializer(ProjectSerializer):
    """Detailed project serializer with nested data"""
    stages = StageSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks with timeline"""
    timeline = TaskTimelineSerializer(required=False)
    
    class Meta:
        model = Task
        fields = [
            'name', 'description', 'project', 'stage', 'status', 'priority',
            'estimated_hours', 'estimated_minutes', 'timeline'
        ]
    
    def create(self, validated_data):
        timeline_data = validated_data.pop('timeline', None)
        task = Task.objects.create(**validated_data)
        
        if timeline_data:
            TaskTimeline.objects.create(task=task, **timeline_data)
        else:
            TaskTimeline.objects.create(task=task)
        
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tasks"""
    timeline = TaskTimelineSerializer(required=False)
    
    class Meta:
        model = Task
        fields = [
            'name', 'description', 'stage', 'status', 'priority',
            'estimated_hours', 'estimated_minutes', 'actual_hours', 'actual_minutes',
            'timeline'
        ]
    
    def update(self, instance, validated_data):
        timeline_data = validated_data.pop('timeline', None)
        
        # Update task
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update timeline if provided
        if timeline_data:
            timeline, created = TaskTimeline.objects.get_or_create(task=instance)
            for attr, value in timeline_data.items():
                setattr(timeline, attr, value)
            timeline.save()
        
        return instance


class TaskDependencyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating task dependencies"""
    class Meta:
        model = TaskDependency
        fields = ['dependent_task', 'prerequisite_task']
    
    def validate(self, data):
        """Custom validation for dependencies"""
        dependent_task = data['dependent_task']
        prerequisite_task = data['prerequisite_task']
        
        # Check if tasks belong to the same project
        if dependent_task.project != prerequisite_task.project:
            raise serializers.ValidationError(
                "Tasks must belong to the same project"
            )
        
        # Check for self-dependency
        if dependent_task == prerequisite_task:
            raise serializers.ValidationError(
                "A task cannot depend on itself"
            )
        
        return data 