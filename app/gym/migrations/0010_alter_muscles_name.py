# Generated by Django 5.0.1 on 2024-04-04 00:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0009_muscles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muscles',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]