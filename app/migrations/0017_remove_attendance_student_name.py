# Generated by Django 5.0.6 on 2024-06-12 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_dailyattendance_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='student_name',
        ),
    ]
