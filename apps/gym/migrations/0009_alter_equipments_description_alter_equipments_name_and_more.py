# Generated by Django 5.0.7 on 2024-07-30 11:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0008_workouthistoryexercises_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipments',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='equipments',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='exercises',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='exercises',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='exercises',
            name='primary_muscle',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='primary_muscle_group',
                to='gym.musclegroups',
                verbose_name='primary muscle',
            ),
        ),
        migrations.AlterField(
            model_name='exercises',
            name='secondary_muscle',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='secondary_muscle_group',
                to='gym.musclegroups',
                verbose_name='secondary muscle',
            ),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='exercise',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='gym.exercises',
                verbose_name='exercise',
            ),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='repetitions',
            field=models.PositiveIntegerField(null=True, verbose_name='repetitions'),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='rest_period',
            field=models.IntegerField(null=True, verbose_name='rest period'),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='sets',
            field=models.PositiveIntegerField(null=True, verbose_name='sets'),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name='user',
            ),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='weight',
            field=models.IntegerField(null=True, verbose_name='weight'),
        ),
        migrations.AlterField(
            model_name='workoutexercises',
            name='workout',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='gym.workouts',
                verbose_name='workout',
            ),
        ),
        migrations.AlterField(
            model_name='workouthistory',
            name='completed_at',
            field=models.DateTimeField(
                blank=True, null=True, verbose_name='completed at'
            ),
        ),
        migrations.AlterField(
            model_name='workouthistory',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='history_created_by',
                to=settings.AUTH_USER_MODEL,
                verbose_name='created by',
            ),
        ),
        migrations.AlterField(
            model_name='workouthistory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='workouthistory',
            name='title',
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name='title'
            ),
        ),
        migrations.AlterField(
            model_name='workouthistory',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
                verbose_name='user',
            ),
        ),
        migrations.AlterField(
            model_name='workouthistory',
            name='workout',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='gym.workouts',
                verbose_name='workout',
            ),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='exercise',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='gym.exercises',
                verbose_name='exercise',
            ),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='name',
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name='name'
            ),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='repetitions',
            field=models.PositiveIntegerField(null=True, verbose_name='repetitions'),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='rest_period',
            field=models.IntegerField(null=True, verbose_name='rest period'),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='sets',
            field=models.PositiveIntegerField(null=True, verbose_name='sets'),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name='user',
            ),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='weight',
            field=models.IntegerField(null=True, verbose_name='weight'),
        ),
        migrations.AlterField(
            model_name='workouthistoryexercises',
            name='workout_history',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='gym.workouthistory',
                verbose_name='workout history',
            ),
        ),
        migrations.AlterField(
            model_name='workouts',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='created_by',
                to=settings.AUTH_USER_MODEL,
                verbose_name='created by',
            ),
        ),
        migrations.AlterField(
            model_name='workouts',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='workouts',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='workouts',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='user',
            ),
        ),
    ]