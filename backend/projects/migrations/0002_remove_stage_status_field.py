# Generated manually to remove stage status field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='status',
        ),
    ]
