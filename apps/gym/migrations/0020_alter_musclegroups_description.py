# Generated by Django 5.0.7 on 2024-08-30 00:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0019_alter_musclegroups_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musclegroups',
            name='description',
            field=models.JSONField(null=True, verbose_name='description'),
        ),
    ]