from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.account.models import EmailAddress
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
import requests
import json
from .models import CustomUser


@api_view(['GET'])
@permission_classes([AllowAny])
def google_oauth_url(request):
    """Get Google OAuth URL for frontend"""
    client_id = settings.SOCIALACCOUNT_PROVIDERS['google'].get('APP', {}).get('client_id')
    if not client_id:
        return Response({'error': 'Google OAuth not configured'}, status=400)
    
    redirect_uri = settings.OAUTH_CALLBACK_URL
    scope = ' '.join(settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE'])
    
    oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope}&"
        f"access_type=online"
    )
    
    return Response({'oauth_url': oauth_url})


@api_view(['POST'])
@permission_classes([AllowAny])
def google_oauth_callback(request):
    """Handle Google OAuth callback and create/authenticate user"""
    try:
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Authorization code required'}, status=400)
        
        # Exchange code for access token
        token_response = exchange_code_for_token(code)
        if not token_response.get('access_token'):
            return Response({'error': 'Failed to get access token'}, status=400)
        
        # Get user info from Google
        user_info = get_google_user_info(token_response['access_token'])
        if not user_info:
            return Response({'error': 'Failed to get user info'}, status=400)
        
        # Create or get user
        user = get_or_create_user(user_info)
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'is_new_user': created
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)


def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    client_id = settings.SOCIALACCOUNT_PROVIDERS['google'].get('APP', {}).get('client_id')
    client_secret = settings.SOCIALACCOUNT_PROVIDERS['google'].get('APP', {}).get('secret')
    
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.OAUTH_CALLBACK_URL,
    }
    
    response = requests.post(token_url, data=data)
    return response.json()


def get_google_user_info(access_token):
    """Get user information from Google"""
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(user_info_url, headers=headers)
    return response.json() if response.status_code == 200 else None


def get_or_create_user(user_info):
    """Create or get user from Google user info"""
    email = user_info.get('email')
    if not email:
        raise ValueError('Email not provided by Google')
    
    # Check if user already exists
    try:
        user = CustomUser.objects.get(email=email)
        return user
    except CustomUser.DoesNotExist:
        pass
    
    # Create new user
    user = CustomUser.objects.create_user(
        email=email,
        username=user_info.get('given_name', '') + user_info.get('family_name', ''),
        first_name=user_info.get('given_name', ''),
        last_name=user_info.get('family_name', ''),
        password=None  # OAuth users don't need password
    )
    
    # Create social account
    social_account = SocialAccount.objects.create(
        user=user,
        provider=GoogleProvider.id,
        uid=user_info.get('id'),
        extra_data=user_info
    )
    
    # Create email address
    EmailAddress.objects.create(
        user=user,
        email=email,
        primary=True,
        verified=True
    )
    
    return user


@api_view(['GET'])
@permission_classes([AllowAny])
def oauth_providers(request):
    """Get available OAuth providers"""
    providers = []
    
    if settings.SOCIALACCOUNT_PROVIDERS.get('google'):
        providers.append({
            'name': 'Google',
            'id': 'google',
            'icon': 'google',
            'color': '#4285F4'
        })
    
    return Response({'providers': providers}) 