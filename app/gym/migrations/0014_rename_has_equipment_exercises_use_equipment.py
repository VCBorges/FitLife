# Generated by Django 5.0.1 on 2024-04-05 11:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0013_delete_muscles_remove_exercises_equipment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercises',
            old_name='has_equipment',
            new_name='use_equipment',
        ),
    ]
