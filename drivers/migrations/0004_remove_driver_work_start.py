# Generated by Django 4.2.16 on 2024-11-17 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0003_rename_duration_course_duration_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='work_start',
        ),
    ]