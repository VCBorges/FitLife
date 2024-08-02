# Generated by Django 5.0.7 on 2024-07-26 10:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutexercises',
            name='exercise',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='gym.exercises'
            ),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='workout',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='gym.workouts'
            ),
        ),
    ]
