#!/usr/bin/env python
"""
Quick authentication test to verify the fix works.
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

from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


def quick_test():
    """Quick authentication test"""
    print("🔍 Quick Authentication Test...")
    print("=" * 35)
    
    # Check if demo user exists
    try:
        user = User.objects.get(email='demo@example.com')
        print(f"✅ User found: {user.email}")
        print(f"   Active: {user.is_active}")
        print(f"   Username: {user.username}")
    except User.DoesNotExist:
        print("❌ Demo user not found!")
        return False
    
    # Test authentication
    print("\n🔐 Testing authentication...")
    auth_user = authenticate(username='demo@example.com', password='demo123')
    
    if auth_user:
        print("✅ Authentication successful!")
        print(f"   Authenticated user: {auth_user.email}")
        return True
    else:
        print("❌ Authentication failed!")
        return False


if __name__ == '__main__':
    success = quick_test()
    if success:
        print("\n🎉 Authentication is working correctly!")
    else:
        print("\n⚠️  Authentication still has issues.")
    sys.exit(0 if success else 1)
