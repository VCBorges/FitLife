# Generated by Django 5.0.7 on 2025-01-09 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_alter_users_height_alter_users_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='phone',
            field=models.CharField(
                blank=True, max_length=15, null=True, verbose_name='phone'
            ),
        ),
    ]
