from __future__ import annotations

from django.db import models

from ..core.models import BaseModel


class MuscleGroups(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'muscle_groups'
        verbose_name = 'Muscle Group'
        verbose_name_plural = 'Muscle Groups'
        default_related_name = 'muscle_groups'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Equipments(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'equipments'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
        default_related_name = 'equipments'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Exercises(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    equipment = models.ForeignKey(
        'gym.Equipments', on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        db_table = 'exercises'
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
        default_related_name = 'exercises'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Workouts(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return self.name


class WorkoutHistory(BaseModel):
    workout = models.ForeignKey('gym.Workouts', on_delete=models.CASCADE)
    finished_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField()
    calories = models.FloatField()

    class Meta:
        db_table = 'workout_history'
        verbose_name = 'Workout History'
        verbose_name_plural = 'Workout Historys'
        default_related_name = 'workout_history'

    def __str__(self):
        return f'{self.workout.name} - {self.executed_at}'


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
        db_table = 'workout_exercises'
        verbose_name = 'Workout Exercise'
        verbose_name_plural = 'Workouts Exercises'
        default_related_name = 'workout_exercises'

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name
