# Generated by Django 5.0.1 on 2024-05-03 22:52

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0028_workouthistoryexercises_rest_period_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymInstructor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GymMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'uuid',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
