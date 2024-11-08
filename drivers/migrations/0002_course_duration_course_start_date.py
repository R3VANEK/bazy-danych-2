# Generated by Django 4.2.16 on 2024-11-08 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
