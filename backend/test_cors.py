#!/usr/bin/env python
"""
Test script to verify CORS configuration is working properly.
Run this script to check if CORS headers are being set correctly.
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dev')
django.setup()

from django.conf import settings
from django.test import RequestFactory
from django.http import JsonResponse
from corsheaders.middleware import CorsMiddleware


def test_cors_headers():
    """Test if CORS headers are being set correctly"""
    print("🔍 Testing CORS Configuration...")
    print("=" * 40)
    
    # Print current CORS settings
    print(f"CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
    print(f"CORS_ALLOW_ALL_ORIGINS: {settings.CORS_ALLOW_ALL_ORIGINS}")
    print(f"CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
    print()
    
    # Create a test request
    factory = RequestFactory()
    request = factory.get('/api/projects/', HTTP_ORIGIN='http://localhost:3000')
    
    # Apply CORS middleware
    middleware = CorsMiddleware(lambda req: JsonResponse({'test': 'success'}))
    response = middleware(request)
    
    # Check CORS headers
    print("📋 CORS Headers in Response:")
    cors_headers = {
        'Access-Control-Allow-Origin': response.get('Access-Control-Allow-Origin'),
        'Access-Control-Allow-Credentials': response.get('Access-Control-Allow-Credentials'),
        'Access-Control-Allow-Methods': response.get('Access-Control-Allow-Methods'),
        'Access-Control-Allow-Headers': response.get('Access-Control-Allow-Headers'),
    }
    
    for header, value in cors_headers.items():
        print(f"  {header}: {value}")
    
    print()
    
    # Test with different origins
    test_origins = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://0.0.0.0:3000',
        'http://invalid-origin.com'
    ]
    
    print("🧪 Testing Different Origins:")
    for origin in test_origins:
        request = factory.get('/api/projects/', HTTP_ORIGIN=origin)
        response = middleware(request)
        allowed = response.get('Access-Control-Allow-Origin')
        print(f"  {origin} -> {allowed}")
    
    print()
    print("✅ CORS test completed!")


if __name__ == '__main__':
    test_cors_headers()
