#!/bin/bash

# Sample Data Setup Script for Project Planning App
# This script sets up demo users, projects, stages, and tasks

echo "🚀 Setting up sample data for Project Planning App..."
echo "=================================================="

# Check if we're in the backend directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   cd backend && ./setup_sample_data.sh"
    exit 1
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed or not in PATH"
    exit 1
fi

# Run the setup
echo "📦 Loading sample data..."
python setup_sample_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Start the backend: python manage.py runserver"
    echo "2. Start the frontend: cd ../frontend && npm run dev"
    echo "3. Login with: demo@example.com / demo123"
    echo ""
    echo "📊 You now have:"
    echo "   • 2 demo users"
    echo "   • 4 sample projects"
    echo "   • 9 stages"
    echo "   • 17 tasks"
    echo "   • Timeline data"
else
    echo "❌ Setup failed. Please check the error messages above."
    exit 1
fi
