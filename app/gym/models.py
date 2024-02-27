from django.db import models

from ..core.models import BaseModel


class Workouts(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(
        'users.Users', on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'
        default_related_name = 'workouts'

    def __str__(self):
        return self.name


class WorkoutHistory(BaseModel):
    workout = models.ForeignKey(Workouts, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.DurationField()
    repetitions = models.IntegerField()
    weight = models.FloatField()
    distance = models.FloatField()
    calories = models.FloatField()

    class Meta:
        verbose_name = 'Workout History'
        verbose_name_plural = 'Workout Historys'
        default_related_name = 'workout_history'

    def __str__(self):
        return f'{self.workout.name} - {self.date}'


class Exercises(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    equipment = models.ForeignKey(
        'gym.Equipments', on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
        default_related_name = 'exercises'

    def __str__(self):
        return self.name


class MuscleGroups(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Muscle Group'
        verbose_name_plural = 'Muscle Groups'
        default_related_name = 'muscle_groups'

    def __str__(self):
        return self.name


class Equipments(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
        default_related_name = 'equipments'

    def __str__(self):
        return self.name
