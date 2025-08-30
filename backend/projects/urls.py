from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'stages', views.StageViewSet, basename='stage')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'timelines', views.TaskTimelineViewSet, basename='timeline')
router.register(r'dependencies', views.TaskDependencyViewSet, basename='dependency')

urlpatterns = [
    path('', include(router.urls)),
] 