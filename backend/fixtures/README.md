# Sample Data Fixtures

This directory contains sample data fixtures for the Project Planning application.

## 📁 Files

- `sample_data.json` - Comprehensive sample data including users, projects, stages, tasks, and timelines

## 🚀 Quick Setup

### Option 1: Using the setup script (Recommended)
```bash
cd backend
python setup_sample_data.py
```

### Option 2: Using Django management command
```bash
cd backend
python manage.py load_sample_data --clear --password=demo123
```

### Option 3: Manual fixture loading
```bash
cd backend
python manage.py loaddata sample_data.json
```

## 👥 Demo Users

| Email | Password | Name |
|-------|----------|------|
| demo@example.com | demo123 | Demo User |
| john.doe@example.com | demo123 | John Doe |

## 📊 Sample Data Overview

### Projects (4 total)
1. **Website Redesign** (Active) - Complete website redesign project
2. **Mobile App Development** (Planning) - Cross-platform mobile app
3. **Database Migration** (In Progress) - Legacy database migration
4. **Marketing Campaign** (Completed) - Q1 marketing campaign

### Stages (9 total)
- **Website Redesign**: 6 stages (Planning → Deployment)
- **Mobile App Development**: 1 stage (Requirements Analysis)
- **Database Migration**: 2 stages (Data Backup → Schema Migration)

### Tasks (17 total)
- Various priorities (Low, Medium, High, Urgent)
- Different statuses (Not Started, In Progress, Completed, etc.)
- Time estimates and actual time tracking
- Some tasks with timeline data

### Task Timelines (6 total)
- Planned start/due dates
- Actual start/completion dates
- Overdue and completed tasks

## 🔧 Customization

### Changing Default Password
```bash
python manage.py load_sample_data --password=your_password
```

### Loading Without Clearing Existing Data
```bash
python manage.py load_sample_data  # Remove --clear flag
```

### Creating Your Own Fixtures
1. Export existing data:
   ```bash
   python manage.py dumpdata users.projects > my_data.json
   ```

2. Load your custom data:
   ```bash
   python manage.py loaddata my_data.json
   ```

## 🧹 Clearing Sample Data

To remove all sample data:
```bash
python manage.py load_sample_data --clear
```

Or manually:
```bash
python manage.py shell
```
```python
from projects.models import *
from django.contrib.auth import get_user_model

User = get_user_model()
TaskTimeline.objects.all().delete()
TaskDependency.objects.all().delete()
Task.objects.all().delete()
Stage.objects.all().delete()
Project.objects.all().delete()
User.objects.filter(email__in=['demo@example.com', 'john.doe@example.com']).delete()
```

## 📝 Notes

- The sample data includes realistic project scenarios
- Tasks have varying priorities and time estimates
- Some tasks include timeline data for testing date functionality
- All data is interconnected with proper foreign key relationships
- The fixtures are designed to work with the current model structure
