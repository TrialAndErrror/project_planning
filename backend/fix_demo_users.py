#!/usr/bin/env python
"""
Script to fix demo user passwords and ensure they can log in properly.
This script will update the demo users with proper passwords and make sure they're active.
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

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


def fix_demo_users():
    """Fix demo users to ensure they can log in"""
    print("🔧 Fixing Demo Users...")
    print("=" * 30)
    
    # Demo user data
    demo_users = [
        {
            'email': 'demo@example.com',
            'username': 'demo_user',
            'first_name': 'Demo',
            'last_name': 'User',
            'password': 'demo123'
        },
        {
            'email': 'john.doe@example.com',
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'demo123'
        }
    ]
    
    for user_data in demo_users:
        email = user_data['email']
        
        try:
            # Try to get existing user
            user = User.objects.get(email=email)
            print(f"📝 Updating existing user: {email}")
            
            # Update user data
            user.username = user_data['username']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            
            # Set password
            user.set_password(user_data['password'])
            user.save()
            
            print(f"✅ Updated user: {email}")
            
        except User.DoesNotExist:
            # Create new user
            print(f"📝 Creating new user: {email}")
            
            user = User.objects.create_user(
                email=email,
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password']
            )
            
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()
            
            print(f"✅ Created user: {email}")
    
    print()
    return True


def test_authentication():
    """Test that users can authenticate"""
    print("🔐 Testing Authentication...")
    print("=" * 30)
    
    test_users = [
        ('demo@example.com', 'demo123'),
        ('john.doe@example.com', 'demo123')
    ]
    
    for email, password in test_users:
        user = authenticate(username=email, password=password)
        if user:
            print(f"✅ Authentication successful: {email}")
        else:
            print(f"❌ Authentication failed: {email}")
            return False
    
    print()
    return True


def main():
    """Main function"""
    print("🚀 Fixing Demo Users for Login...")
    print("=" * 50)
    
    try:
        # Fix demo users
        if not fix_demo_users():
            print("❌ Failed to fix demo users")
            return False
        
        # Test authentication
        if not test_authentication():
            print("❌ Authentication test failed")
            return False
        
        print("🎉 Demo users fixed successfully!")
        print("\n📋 Login Credentials:")
        print("  • Email: demo@example.com, Password: demo123")
        print("  • Email: john.doe@example.com, Password: demo123")
        print("\n🔗 You can now log in to the application!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    main()
