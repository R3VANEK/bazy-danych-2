# Generated by Django 4.2.16 on 2024-11-17 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='gender',
            new_name='is_male',
        ),
    ]
