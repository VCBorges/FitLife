# Generated by Django 5.0.7 on 2024-08-14 10:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0009_alter_equipments_description_alter_equipments_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workouts',
            name='created_by',
        ),
        migrations.AddField(
            model_name='workouts',
            name='creator',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='creator',
                to=settings.AUTH_USER_MODEL,
                verbose_name='creator',
            ),
        ),
    ]
