from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.utils import timezone
from .models import Project, Stage, Task, TaskTimeline, TaskDependency
from .serializers import (
    ProjectSerializer, ProjectDetailSerializer, StageSerializer, StageCreateSerializer,
    TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer,
    TaskTimelineSerializer, TaskDependencySerializer, TaskDependencyCreateSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for projects"""
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Return projects owned by the current user"""
        return Project.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve actions"""
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        """Set the owner when creating a project"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get timeline view of project tasks"""
        project = self.get_object()
        tasks = project.tasks.select_related('timeline').all()
        
        timeline_data = []
        for task in tasks:
            timeline = task.timeline
            if timeline:
                timeline_data.append({
                    'task_id': task.id,
                    'task_name': task.name,
                    'planned_start_date': timeline.planned_start_date,
                    'planned_due_date': timeline.planned_due_date,
                    'actual_start_date': timeline.actual_start_date,
                    'actual_completion_date': timeline.actual_completion_date,
                    'status': task.status,
                    'priority': task.priority,
                    'is_overdue': timeline.is_overdue,
                })
        
        return Response(timeline_data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get project statistics"""
        project = self.get_object()
        
        total_tasks = project.tasks.count()
        completed_tasks = project.tasks.filter(status='completed').count()
        overdue_tasks = sum(1 for task in project.tasks.all() if task.timeline.is_overdue)
        
        # Calculate total estimated vs actual time
        total_estimated_minutes = sum(task.estimated_time_minutes for task in project.tasks.all())
        total_actual_minutes = sum(task.actual_time_minutes for task in project.tasks.all())
        
        stats = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks,
            'progress_percentage': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
            'total_estimated_hours': total_estimated_minutes // 60,
            'total_estimated_minutes': total_estimated_minutes % 60,
            'total_actual_hours': total_actual_minutes // 60,
            'total_actual_minutes': total_actual_minutes % 60,
        }
        
        return Response(stats)


class StageViewSet(viewsets.ModelViewSet):
    """ViewSet for stages"""
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Return stages for projects owned by the current user"""
        return Stage.objects.filter(project__owner=self.request.user)
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action"""
        if self.action == 'create':
            return StageCreateSerializer
        return StageSerializer
    
    def perform_create(self, serializer):
        """Set the owner when creating a stage"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        """Reorder stages within a project"""
        stage = self.get_object()
        new_order = request.data.get('order')
        
        if new_order is not None:
            # Update the order of this stage and adjust others
            old_order = stage.order
            project = stage.project
            
            if new_order > old_order:
                # Moving down - shift others up
                Stage.objects.filter(
                    project=project,
                    order__gt=old_order,
                    order__lte=new_order
                ).update(order=models.F('order') - 1)
            else:
                # Moving up - shift others down
                Stage.objects.filter(
                    project=project,
                    order__gte=new_order,
                    order__lt=old_order
                ).update(order=models.F('order') + 1)
            
            stage.order = new_order
            stage.save()
            
            return Response({'status': 'reordered'})
        
        return Response({'error': 'order parameter required'}, status=400)


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for tasks"""
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Return tasks for projects owned by the current user"""
        return Task.objects.filter(project__owner=self.request.user)
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action"""
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        """Set the owner when creating a task"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Mark task as started"""
        task = self.get_object()
        timeline, created = TaskTimeline.objects.get_or_create(task=task)
        
        if not timeline.actual_start_date:
            timeline.actual_start_date = timezone.now()
            timeline.save()
            task.status = 'in_progress'
            task.save()
        
        return Response({'status': 'started'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed"""
        task = self.get_object()
        timeline, created = TaskTimeline.objects.get_or_create(task=task)
        
        timeline.actual_completion_date = timezone.now()
        timeline.save()
        task.status = 'completed'
        task.save()
        
        return Response({'status': 'completed'})
    
    @action(detail=True, methods=['post'])
    def add_time(self, request, pk=None):
        """Add actual time to task"""
        task = self.get_object()
        hours = request.data.get('hours', 0)
        minutes = request.data.get('minutes', 0)
        
        # Validate 15-minute increments
        if minutes % 15 != 0:
            return Response(
                {'error': 'Minutes must be in 15-minute increments'}, 
                status=400
            )
        
        task.actual_hours += hours
        task.actual_minutes += minutes
        
        # Convert excess minutes to hours
        if task.actual_minutes >= 60:
            task.actual_hours += task.actual_minutes // 60
            task.actual_minutes = task.actual_minutes % 60
        
        task.save()
        
        return Response({
            'actual_hours': task.actual_hours,
            'actual_minutes': task.actual_minutes,
            'actual_time_formatted': task.actual_time_formatted
        })
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue tasks"""
        overdue_tasks = []
        for task in self.get_queryset():
            if task.timeline.is_overdue:
                overdue_tasks.append(TaskSerializer(task).data)
        
        return Response(overdue_tasks)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming tasks (due in next 7 days)"""
        upcoming_tasks = []
        seven_days_from_now = timezone.now() + timezone.timedelta(days=7)
        
        for task in self.get_queryset():
            timeline = task.timeline
            if (timeline.planned_due_date and 
                timeline.planned_due_date <= seven_days_from_now and
                not timeline.actual_completion_date):
                upcoming_tasks.append(TaskSerializer(task).data)
        
        return Response(upcoming_tasks)


class TaskTimelineViewSet(viewsets.ModelViewSet):
    """ViewSet for task timelines"""
    serializer_class = TaskTimelineSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Return timelines for tasks owned by the current user"""
        return TaskTimeline.objects.filter(task__project__owner=self.request.user)


class TaskDependencyViewSet(viewsets.ModelViewSet):
    """ViewSet for task dependencies"""
    serializer_class = TaskDependencySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return dependencies for tasks owned by the current user"""
        return TaskDependency.objects.filter(
            dependent_task__project__owner=self.request.user
        )
    
    def get_serializer_class(self):
        """Use create serializer for creation"""
        if self.action == 'create':
            return TaskDependencyCreateSerializer
        return TaskDependencySerializer
    
    def perform_create(self, serializer):
        """Validate and create dependency"""
        try:
            serializer.save()
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            ) 