# Generated by Django 3.2.25 on 2024-11-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0003_alter_driver_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
    ]
