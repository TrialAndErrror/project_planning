#!/bin/bash

# Environment switcher script for project planning

set -e

function show_usage() {
    echo "Usage: $0 [dev|prod]"
    echo ""
    echo "Commands:"
    echo "  dev   - Switch to development environment"
    echo "  prod  - Switch to production environment"
    echo ""
    echo "Examples:"
    echo "  $0 dev   # Switch to development"
    echo "  $0 prod  # Switch to production"
}

function switch_to_dev() {
    echo "🔄 Switching to development environment..."
    
    # Copy development environment file
    if [ -f "env.dev" ]; then
        cp env.dev .env
        echo "✅ Copied env.dev to .env"
    else
        echo "❌ env.dev file not found"
        exit 1
    fi
    
    echo ""
    echo "🚀 To start development environment:"
    echo "   docker-compose -f docker-compose.dev.yml up --build"
    echo ""
    echo "📝 Development features:"
    echo "   - Hot reloading enabled"
    echo "   - Debug mode on"
    echo "   - Console email backend"
    echo "   - Volume mounts for live changes"
}

function switch_to_prod() {
    echo "🔄 Switching to production environment..."
    
    # Check if .env already exists
    if [ -f ".env" ]; then
        echo "⚠️  .env file already exists. Please review and update it manually."
        echo "   Template available in env.prod"
    else
        # Copy production environment template
        if [ -f "env.prod" ]; then
            cp env.prod .env
            echo "✅ Copied env.prod to .env"
            echo "⚠️  IMPORTANT: Please edit .env with your production values!"
        else
            echo "❌ env.prod file not found"
            exit 1
        fi
    fi
    
    echo ""
    echo "🚀 To start production environment:"
    echo "   docker-compose up --build -d"
    echo ""
    echo "📝 Production features:"
    echo "   - Gunicorn WSGI server"
    echo "   - Lightweight HTTP server"
    echo "   - SSL support (configure with Caddy)"
    echo "   - Security headers"
    echo "   - File logging"
}

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "❌ No environment specified"
    show_usage
    exit 1
fi

# Parse command
case $1 in
    dev)
        switch_to_dev
        ;;
    prod)
        switch_to_prod
        ;;
    *)
        echo "❌ Invalid environment: $1"
        show_usage
        exit 1
        ;;
esac 