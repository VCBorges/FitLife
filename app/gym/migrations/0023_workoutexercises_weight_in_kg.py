# Generated by Django 5.0.1 on 2024-04-22 23:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0022_rename_finished_at_workouthistory_completed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutexercises',
            name='weight_in_kg',
            field=models.IntegerField(null=True),
        ),
    ]
