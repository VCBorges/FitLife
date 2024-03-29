# Generated by Django 5.0.1 on 2024-03-21 23:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0006_remove_workouthistory_distance_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='equipmentmusclegroups',
            table='equipment_muscle_groups',
        ),
        migrations.AlterModelTable(
            name='equipments',
            table='equipments',
        ),
        migrations.AlterModelTable(
            name='exercisemusclegroups',
            table='exercise_muscle_groups',
        ),
        migrations.AlterModelTable(
            name='exercises',
            table='exercises',
        ),
        migrations.AlterModelTable(
            name='musclegroups',
            table='muscle_groups',
        ),
        migrations.AlterModelTable(
            name='workoutexercises',
            table='workout_exercises',
        ),
        migrations.AlterModelTable(
            name='workouthistory',
            table='workout_history',
        ),
        migrations.AlterModelTable(
            name='workouthistoryexercises',
            table='workout_history_exercises',
        ),
        migrations.AlterModelTable(
            name='workouts',
            table='workouts',
        ),
    ]
