# Project Planning - Django + Vue.js

A full-stack project management application built with Django backend and Vue.js frontend, containerized with Docker Compose.

## Features

- **Authentication System**: User registration and login with email/password
- **OAuth Integration**: Google OAuth support for easy sign-in
- **Modern UI**: Beautiful, responsive interface built with Vue 3 and Vite
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

2. **Configure OAuth (Optional but Recommended)**
   
   To enable Google OAuth:
   
   a. Go to [Google Cloud Console](https://console.cloud.google.com/)
   b. Create a new project or select existing one
   c. Enable Google+ API
   d. Create OAuth 2.0 credentials
   e. Add authorized redirect URI: `http://localhost:3000/oauth/callback`
   f. Copy your Client ID and Client Secret
   
   Create a `.env` file in the `backend/` directory:
   ```bash
   cp backend/env.example backend/.env
   ```
   
   Edit `backend/.env` and add your Google OAuth credentials:
   ```
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

3. **Start the services**
   ```bash
   docker-compose up --build
   ```

4. **Run database migrations** (in a new terminal)
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Create a superuser** (optional)
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. **Access the application**
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

### OAuth
- `GET /api/users/oauth/providers/` - Get available OAuth providers
- `GET /api/users/oauth/google/url/` - Get Google OAuth URL
- `POST /api/users/oauth/google/callback/` - Handle Google OAuth callback

### User Management
- `GET /api/users/profile/` - Get user profile (authenticated)
- `GET /api/users/auth-status/` - Check authentication status

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

### Email/Password Authentication
1. User registers with email and password
2. Django creates user account and returns authentication token
3. Frontend stores token in localStorage
4. Token is sent with subsequent API requests
5. Django validates token and returns user data

### OAuth Authentication
1. User clicks "Continue with Google" button
2. Frontend redirects to Google OAuth consent screen
3. User authorizes the application
4. Google redirects back to frontend with authorization code
5. Frontend sends code to Django backend
6. Backend exchanges code for access token and gets user info
7. Backend creates/updates user account and returns authentication token
8. Frontend stores token and redirects to dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 