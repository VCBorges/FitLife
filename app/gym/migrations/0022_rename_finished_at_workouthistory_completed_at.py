# Generated by Django 5.0.1 on 2024-04-19 22:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0021_remove_workouthistory_calories_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workouthistory',
            old_name='finished_at',
            new_name='completed_at',
        ),
    ]