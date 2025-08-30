# Deployment Guide

This project supports both development and production deployments with separate configurations.

## File Structure

```
├── docker-compose.yml          # Production configuration
├── docker-compose.dev.yml      # Development configuration
├── backend/core/settings.py    # Production settings
├── backend/core/settings_dev.py # Development settings
├── env.dev                     # Development environment variables
├── env.prod                    # Production environment variables template
└── frontend/Dockerfile.prod    # Production frontend Dockerfile
```

## Development Setup

### 1. Start Development Environment

```bash
# Copy development environment file
cp env.dev .env

# Start development services
docker-compose -f docker-compose.dev.yml up --build
```

### 2. Development Features

- **Hot reloading** for both frontend and backend
- **Console email backend** - emails are printed to console
- **Debug mode enabled** for detailed error messages
- **Volume mounts** for live code changes
- **Development database** with sample data

### 3. Access Development Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: localhost:5432

## Production Setup

### 1. Environment Configuration

```bash
# Copy production environment template
cp env.prod .env

# Edit .env with your production values
nano .env
```

**Required Production Values:**
- `SECRET_KEY`: Generate a secure Django secret key
- `DJANGO_ALLOWED_HOSTS`: Your domain names
- `POSTGRES_PASSWORD`: Secure database password
- `EMAIL_HOST_USER`: Your email address
- `EMAIL_HOST_PASSWORD`: Your email app password
- `CORS_ALLOWED_ORIGINS`: Your domain URLs
- `VITE_API_URL`: Your production API URL

### 2. Generate Django Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Start Production Environment

```bash
# Start production services
docker-compose up --build -d
```

### 4. Production Features

- **Gunicorn** WSGI server for Django
- **Lightweight HTTP server** for static file serving
- **Production database** with proper security
- **Email verification** with SMTP
- **Static file serving** with caching
- **Security headers**
- **Logging** to files and console

### 5. SSL Configuration (Optional)

To enable HTTPS, configure your personal Caddy server to handle SSL termination and proxy requests to the application containers.

## Environment Variables

### Development (.env)
```bash
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-development
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_PASSWORD=postgres
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
CORS_ALLOWED_ORIGINS=http://localhost:3000
VITE_API_URL=http://localhost:8000
```

### Production (.env)
```bash
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DJANGO_ALLOWED_HOSTS=yourdomain.com www.yourdomain.com
POSTGRES_PASSWORD=your-secure-database-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CORS_ALLOWED_ORIGINS=https://yourdomain.com
VITE_API_URL=https://yourdomain.com
```

## Database Management

### Development
```bash
# Access Django shell
docker-compose -f docker-compose.dev.yml exec backend python manage.py shell

# Run migrations
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate

# Create superuser
docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
```

### Production
```bash
# Access Django shell
docker-compose exec backend python manage.py shell

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

## Monitoring and Logs

### Development
```bash
# View all logs
docker-compose -f docker-compose.dev.yml logs -f

# View specific service logs
docker-compose -f docker-compose.dev.yml logs -f backend
```

### Production
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
```

## Backup and Restore

### Database Backup
```bash
# Development
docker-compose -f docker-compose.dev.yml exec db pg_dump -U postgres project_planning > backup_dev.sql

# Production
docker-compose exec db pg_dump -U postgres project_planning_prod > backup_prod.sql
```

### Database Restore
```bash
# Development
docker-compose -f docker-compose.dev.yml exec -T db psql -U postgres project_planning < backup_dev.sql

# Production
docker-compose exec -T db psql -U postgres project_planning_prod < backup_prod.sql
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 8000, and 5432 are available
2. **Permission errors**: Run `sudo chown -R $USER:$USER .` in project directory
3. **Database connection**: Check if PostgreSQL container is running
4. **Email issues**: Verify SMTP settings in production

### Reset Development Environment
```bash
# Stop and remove all containers
docker-compose -f docker-compose.dev.yml down -v

# Rebuild and start
docker-compose -f docker-compose.dev.yml up --build
```

### Reset Production Environment
```bash
# Stop and remove all containers
docker-compose down -v

# Rebuild and start
docker-compose up --build -d
```

## Security Checklist

### Development
- [ ] Use different secret key than production
- [ ] Disable debug mode in production
- [ ] Use secure database passwords
- [ ] Configure proper CORS settings

### Production
- [ ] Generate secure Django secret key
- [ ] Set DEBUG=False
- [ ] Configure SSL certificates
- [ ] Set up proper email SMTP
- [ ] Use strong database passwords
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Database backups
- [ ] Rate limiting enabled 