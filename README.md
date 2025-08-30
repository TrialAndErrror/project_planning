# Project Planning - Django + Vue.js

A full-stack project management application built with Django backend and Vue.js frontend, containerized with Docker Compose.

## Features

- **Authentication System**: User registration and login with email/password
- **Project Planning**: Comprehensive project management with stages, tasks, and timelines
- **Time Tracking**: 15-minute increment time estimates and actual time tracking
- **Task Dependencies**: Manage task dependencies and prevent circular dependencies
- **Progress Tracking**: Automatic calculation of project and stage progress
- **Modern UI**: Beautiful, responsive interface built with Vue 3 and Vite
- **Tree View Interface**: Visual project structure with stages and tasks
- **Modal Editing**: In-place editing of projects, stages, and tasks
- **Real-time Updates**: Live project statistics and progress tracking
- **RESTful API**: Django REST Framework backend with token authentication
- **Database**: PostgreSQL for reliable data storage
- **Containerized**: Easy deployment with Docker Compose

## Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework
- PostgreSQL
- dj-rest-auth for authentication
- django-cors-headers for CORS

### Frontend
- Vue 3 with Composition API
- Vue Router for navigation
- Pinia for state management
- Vite for build tooling
- Axios for API communication

### Infrastructure
- Docker & Docker Compose
- PostgreSQL 15

## Quick Start

### Prerequisites
- Docker
- Docker Compose

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project_planning
   ```

2. **Start the services**
   ```bash
   docker-compose up --build
   ```

3. **Run database migrations** (in a new terminal)
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

4. **Create a superuser** (optional)
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Django Admin: http://localhost:8000/admin

## Project Structure

```
project_planning/
├── docker-compose.yml          # Docker Compose configuration
├── backend/                    # Django backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── core/                   # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── users/                  # User management app
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       └── urls.py
└── frontend/                   # Vue.js frontend
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/
        │   └── index.js
        ├── stores/
        │   └── auth.js
        └── views/
            ├── Home.vue
            ├── Login.vue
            └── Register.vue
```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/registration/` - User registration

### User Management
- `GET /api/users/profile/` - Get user profile (authenticated)
- `GET /api/users/auth-status/` - Check authentication status

### Project Management
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}/` - Get project details
- `GET /api/projects/{id}/timeline/` - Get project timeline
- `GET /api/projects/{id}/statistics/` - Get project statistics

### Stage Management
- `GET /api/stages/` - List all stages
- `POST /api/stages/` - Create a new stage
- `POST /api/stages/{id}/reorder/` - Reorder stages

### Task Management
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `POST /api/tasks/{id}/start/` - Start a task
- `POST /api/tasks/{id}/complete/` - Complete a task
- `POST /api/tasks/{id}/add_time/` - Add time to task
- `GET /api/tasks/overdue/` - Get overdue tasks
- `GET /api/tasks/upcoming/` - Get upcoming tasks

### Timeline & Dependencies
- `GET /api/timelines/` - List all timelines
- `GET /api/dependencies/` - List all dependencies
- `POST /api/dependencies/` - Create task dependency

## Development

### Backend Development
```bash
# Access Django shell
docker-compose exec backend python manage.py shell

# Run tests
docker-compose exec backend python manage.py test

# Make migrations
docker-compose exec backend python manage.py makemigrations
```

### Frontend Development
```bash
# Install dependencies (if developing outside Docker)
cd frontend
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Environment Variables

### Backend (.env file in backend directory)
```
DEBUG=1
SECRET_KEY=your-secret-key
POSTGRES_DB=project_planning
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Frontend (.env file in frontend directory)
```
VITE_API_URL=http://localhost:8000
```

## Authentication Flow

1. User registers with email and password
2. Django creates user account and returns authentication token
3. Frontend stores token in localStorage
4. Token is sent with subsequent API requests
5. Django validates token and returns user data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 