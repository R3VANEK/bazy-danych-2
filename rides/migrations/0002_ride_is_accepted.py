# Generated by Django 4.2.16 on 2025-01-03 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
