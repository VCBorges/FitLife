# Generated by Django 5.0.1 on 2024-02-26 22:48

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Equipments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Equipment',
                'verbose_name_plural': 'Equipments',
                'default_related_name': 'equipments',
            },
        ),
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Exercise',
                'verbose_name_plural': 'Exercises',
                'default_related_name': 'exercises',
            },
        ),
        migrations.CreateModel(
            name='MuscleGroups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Muscle Group',
                'verbose_name_plural': 'Muscle Groups',
                'default_related_name': 'muscle_groups',
            },
        ),
        migrations.CreateModel(
            name='Workouts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkoutHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('duration', models.DurationField()),
                ('repetitions', models.IntegerField()),
                ('weight', models.FloatField()),
                ('distance', models.FloatField()),
                ('calories', models.FloatField()),
                (
                    'workout',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='workout_history',
                        to='gym.workouts',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Workout History',
                'verbose_name_plural': 'Workout Historys',
                'default_related_name': 'workout_history',
            },
        ),
    ]