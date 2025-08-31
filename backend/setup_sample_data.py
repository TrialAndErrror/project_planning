#!/usr/bin/env python
"""
Simple script to set up sample data for the project planning application.
This script will create demo users, projects, stages, and tasks for testing.
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.core.management.base import CommandError


def main():
    """Main function to set up sample data"""
    print("🚀 Setting up sample data for Project Planning App...")
    print("=" * 50)
    
    try:
        # Run the load_sample_data command
        execute_from_command_line([
            'manage.py',
            'load_sample_data',
            '--clear',
            '--password=demo123'
        ])
        
        print("\n" + "=" * 50)
        print("✅ Sample data setup completed successfully!")
        print("\n📋 Quick Start Guide:")
        print("1. Start the backend server: python manage.py runserver")
        print("2. Start the frontend: npm run dev (from frontend directory)")
        print("3. Login with:")
        print("   • Email: demo@example.com")
        print("   • Password: demo123")
        print("\n🎯 You'll have access to:")
        print("   • 4 sample projects with different statuses")
        print("   • 9 stages across the projects")
        print("   • 17 tasks with various priorities and time estimates")
        print("   • Timeline data for some tasks")
        
    except CommandError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
