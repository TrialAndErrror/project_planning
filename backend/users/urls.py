from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('auth-status/', views.auth_status, name='auth_status'),
] 