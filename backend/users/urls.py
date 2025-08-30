from django.urls import path
from . import views, oauth_views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('auth-status/', views.auth_status, name='auth_status'),
    path('oauth/google/url/', oauth_views.google_oauth_url, name='google_oauth_url'),
    path('oauth/google/callback/', oauth_views.google_oauth_callback, name='google_oauth_callback'),
    path('oauth/providers/', oauth_views.oauth_providers, name='oauth_providers'),
] 