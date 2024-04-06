from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.core.models import BaseModel


class MuscleGroups(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa

    class Meta:
        db_table = 'muscle_groups'
        verbose_name = 'Muscle Group'
        verbose_name_plural = 'Muscle Groups'
        default_related_name = 'muscle_groups'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Equipments(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa

    class Meta:
        db_table = 'equipments'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
        default_related_name = 'equipments'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Exercises(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa
    primary_muscle = models.ForeignKey(
        'gym.MuscleGroups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_muscle_group',
    )
    secondary_muscle = models.ForeignKey(
        'gym.MuscleGroups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secondary_muscle_group',
    )
    use_equipment = models.BooleanField(default=False)

    class Meta:
        db_table = 'exercises'
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
        default_related_name = 'exercises'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Workouts(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa
    user = models.ForeignKey(
        'users.Users',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'workouts'
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'
        default_related_name = 'workouts'


class WorkoutHistory(BaseModel):
    name = models.CharField(_('name'), max_length=255, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa
    workout = models.ForeignKey('gym.Workouts', on_delete=models.CASCADE)
    finished_at = models.DateTimeField(_('finished at'), null=True, blank=True)
    duration = models.DurationField(_('duration'))
    calories = models.FloatField(_('calories'))

    class Meta:
        db_table = 'workout_history'
        verbose_name = 'Workout History'
        verbose_name_plural = 'Workout Historys'
        default_related_name = 'workout_history'


class WorkoutExercises(BaseModel):
    workout: Workouts = models.ForeignKey(
        'gym.Workouts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exercise: Exercises = models.ForeignKey(
        'gym.Exercises',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    repetitions = models.PositiveIntegerField(null=True)
    sets = models.PositiveIntegerField(null=True)  # series
    rest_period = models.DurationField(null=True)

    class Meta:
        db_table = 'workout_efrom django.utils.translation import gettext_lazy as _xercises'
        verbose_name = 'Workout Exercise'
        verbose_name_plural = 'Workouts Exercises'
        default_related_name = 'workout_exercises'


class ExerciseMuscleGroups(BaseModel):
    exercise = models.ForeignKey(
        'gym.Exercises',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    muscle_group = models.ForeignKey(
        'gym.MuscleGroups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'exercise_muscle_groups'
        verbose_name = 'Exercise Muscle Group'
        verbose_name_plural = 'Exercise Muscle Groups'
        default_related_name = 'exercise_muscle_groups'


class WorkoutHistoryExercises(BaseModel):
    workout_history = models.ForeignKey(
        'gym.WorkoutHistory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exercise = models.ForeignKey(
        'gym.Exercises',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    repetitions = models.PositiveIntegerField(null=True)
    sets = models.PositiveIntegerField(null=True)  # series
    rest_period = models.DurationField(null=True)

    class Meta:
        db_table = 'workout_history_exercises'
        verbose_name = 'Workout History Exercise'
        verbose_name_plural = 'Workout History Exercises'
        default_related_name = 'workout_history_exercises'

    # def __str__(self):
    #     return self.name


class EquipmentMuscleGroups(BaseModel):
    equipment = models.ForeignKey(
        'gym.Equipments',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    muscle_group = models.ForeignKey(
        'gym.MuscleGroups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'equipment_muscle_groups'
        verbose_name = 'Equipment Muscle Group'
        verbose_name_plural = 'Equipment Muscle Groups'
        default_related_name = 'equipment_muscle_groups'
