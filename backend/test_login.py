#!/usr/bin/env python
"""
Test script to verify login functionality with sample data.
This script will test the authentication system with the demo users.
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
from django.test import RequestFactory
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


def test_user_creation():
    """Test if demo users exist and can be authenticated"""
    print("🔍 Testing User Authentication...")
    print("=" * 40)
    
    # Check if demo users exist
    try:
        demo_user = User.objects.get(email='demo@example.com')
        print(f"✅ Demo user found: {demo_user.email}")
        print(f"   Username: {demo_user.username}")
        print(f"   Is active: {demo_user.is_active}")
        print(f"   Is staff: {demo_user.is_staff}")
    except User.DoesNotExist:
        print("❌ Demo user not found!")
        return False
    
    try:
        john_user = User.objects.get(email='john.doe@example.com')
        print(f"✅ John user found: {john_user.email}")
        print(f"   Username: {john_user.username}")
        print(f"   Is active: {john_user.is_active}")
    except User.DoesNotExist:
        print("❌ John user not found!")
        return False
    
    print()
    return True


def test_authentication():
    """Test authentication with demo users"""
    print("🔐 Testing Authentication...")
    print("=" * 30)
    
    # Test demo user authentication
    demo_user = authenticate(username='demo@example.com', password='demo123')
    if demo_user:
        print(f"✅ Demo user authentication successful: {demo_user.email}")
    else:
        print("❌ Demo user authentication failed!")
        return False
    
    # Test john user authentication
    john_user = authenticate(username='john.doe@example.com', password='demo123')
    if john_user:
        print(f"✅ John user authentication successful: {john_user.email}")
    else:
        print("❌ John user authentication failed!")
        return False
    
    print()
    return True


def test_api_login():
    """Test API login endpoints"""
    print("🌐 Testing API Login...")
    print("=" * 25)
    
    client = APIClient()
    
    # Test login endpoint
    login_data = {
        'email': 'demo@example.com',
        'password': 'demo123'
    }
    
    response = client.post('/api/auth/login/', login_data)
    
    if response.status_code == status.HTTP_200_OK:
        print("✅ API login successful!")
        print(f"   Response: {response.data}")
        
        # Test authenticated request
        token = response.data.get('key')
        if token:
            client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            auth_response = client.get('/api/users/auth-status/')
            
            if auth_response.status_code == status.HTTP_200_OK:
                print("✅ Authenticated request successful!")
                print(f"   Auth status: {auth_response.data}")
            else:
                print(f"❌ Authenticated request failed: {auth_response.status_code}")
                print(f"   Response: {auth_response.data}")
        else:
            print("❌ No token in login response!")
            return False
    else:
        print(f"❌ API login failed: {response.status_code}")
        print(f"   Response: {response.data}")
        return False
    
    print()
    return True


def test_invalid_credentials():
    """Test login with invalid credentials"""
    print("🚫 Testing Invalid Credentials...")
    print("=" * 35)
    
    client = APIClient()
    
    # Test with wrong password
    login_data = {
        'email': 'demo@example.com',
        'password': 'wrongpassword'
    }
    
    response = client.post('/api/auth/login/', login_data)
    
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        print("✅ Invalid credentials properly rejected!")
        print(f"   Response: {response.data}")
    else:
        print(f"❌ Invalid credentials not properly handled: {response.status_code}")
        print(f"   Response: {response.data}")
        return False
    
    # Test with non-existent user
    login_data = {
        'email': 'nonexistent@example.com',
        'password': 'demo123'
    }
    
    response = client.post('/api/auth/login/', login_data)
    
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        print("✅ Non-existent user properly rejected!")
        print(f"   Response: {response.data}")
    else:
        print(f"❌ Non-existent user not properly handled: {response.status_code}")
        print(f"   Response: {response.data}")
        return False
    
    print()
    return True


def main():
    """Main test function"""
    print("🚀 Testing Login Functionality...")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("User Creation", test_user_creation),
        ("Authentication", test_authentication),
        ("API Login", test_api_login),
        ("Invalid Credentials", test_invalid_credentials),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Login functionality is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == len(results)


if __name__ == '__main__':
    main()
