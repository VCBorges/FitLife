# Generated by Django 5.0.7 on 2024-10-30 16:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_remove_users_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='height',
            field=models.IntegerField(blank=True, null=True, verbose_name='height'),
        ),
        migrations.AlterField(
            model_name='users',
            name='weight',
            field=models.IntegerField(blank=True, null=True, verbose_name='weight'),
        ),
    ]