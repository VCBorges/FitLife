# Generated by Django 5.0.1 on 2024-04-07 01:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0015_alter_musclegroups_description_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='workoutexercises',
            table='workout_exercises',
        ),
    ]