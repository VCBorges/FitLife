# Generated by Django 5.0.1 on 2024-04-25 21:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0026_rename_name_workouts_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workouthistory',
            old_name='name',
            new_name='title',
        ),
    ]