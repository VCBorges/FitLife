# Generated by Django 5.0.7 on 2024-08-28 00:40

from django.db import migrations, models

import apps.core.utils


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0012_remove_exercises_use_equipment_exercises_equipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipments',
            name='translations',
            field=models.JSONField(
                default=apps.core.utils.default_translation, verbose_name='translation'
            ),
        ),
        migrations.AddField(
            model_name='musclegroups',
            name='translations',
            field=models.JSONField(
                default=apps.core.utils.default_translation, verbose_name='translation'
            ),
        ),
    ]
