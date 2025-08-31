from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Load sample data including users, projects, stages, and tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading sample data',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='demo123',
            help='Password for demo users (default: demo123)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load sample data...'))
        
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_existing_data()
        
        # Load fixtures
        try:
            call_command('loaddata', 'sample_data.json', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✓ Sample data loaded successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error loading fixtures: {e}'))
            return
        
        # Update passwords for demo users
        self.update_user_passwords(options['password'])
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data setup complete!'))
        self.stdout.write('\nDemo accounts:')
        self.stdout.write('  • Email: demo@example.com, Password: ' + options['password'])
        self.stdout.write('  • Email: john.doe@example.com, Password: ' + options['password'])
        self.stdout.write('\nSample projects:')
        self.stdout.write('  • Website Redesign (Active)')
        self.stdout.write('  • Mobile App Development (Planning)')
        self.stdout.write('  • Database Migration (In Progress)')
        self.stdout.write('  • Marketing Campaign (Completed)')

    def clear_existing_data(self):
        """Clear existing data from the database"""
        with transaction.atomic():
            # Clear in reverse order to avoid foreign key constraints
            from projects.models import TaskTimeline, TaskDependency, Task, Stage, Project
            
            TaskTimeline.objects.all().delete()
            TaskDependency.objects.all().delete()
            Task.objects.all().delete()
            Stage.objects.all().delete()
            Project.objects.all().delete()
            User.objects.filter(email__in=['demo@example.com', 'john.doe@example.com']).delete()
            
            self.stdout.write('✓ Existing data cleared')

    def update_user_passwords(self, password):
        """Update passwords for demo users"""
        try:
            demo_user = User.objects.get(email='demo@example.com')
            demo_user.set_password(password)
            demo_user.save()
            
            john_user = User.objects.get(email='john.doe@example.com')
            john_user.set_password(password)
            john_user.save()
            
            self.stdout.write('✓ User passwords updated')
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('⚠ Demo users not found, skipping password update'))
