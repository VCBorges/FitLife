# Generated by Django 5.0.7 on 2024-08-30 00:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0023_equipments_description_equipments_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercises',
            name='description',
        ),
        migrations.RemoveField(
            model_name='exercises',
            name='name',
        ),
    ]