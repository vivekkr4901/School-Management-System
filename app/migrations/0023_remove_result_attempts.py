# Generated by Django 5.0.6 on 2024-06-24 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_result_attempts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='attempts',
        ),
    ]
