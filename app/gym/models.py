from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.core.models import BaseModel
from app.users.models import Users


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
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # ruff: noqa

    class Meta:
        db_table = 'equipments'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
        default_related_name = 'equipments'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Exercises(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # ruff: noqa
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
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # ruff: noqa
    user: Users = models.ForeignKey(
        'users.Users',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_by: Users = models.ForeignKey(
        'users.Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_by',
    )

    class Meta:
        db_table = 'workouts'
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'
        default_related_name = 'workouts'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.title}>'

    @property
    def exercises(self) -> models.QuerySet[WorkoutExercises]:
        return self.workout_exercises


# TODO: Fix the plural name to <Histories>
class WorkoutHistory(BaseModel):
    user = models.ForeignKey(
        'users.Users',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # ruff: noqa
    workout = models.ForeignKey(
        'gym.Workouts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    # duration = models.DurationField()
    # calories = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'workout_history'
        verbose_name = 'Workout History'
        verbose_name_plural = 'Workout Historys'
        default_related_name = 'workout_history'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.title} {self.completed_at}>'

    @property
    def exercises(self) -> models.QuerySet[WorkoutHistoryExercises]:
        return self.workout_history_exercises


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
    weight_in_kg = models.IntegerField(null=True)
    rest_period = models.IntegerField(null=True)

    class Meta:
        db_table = 'workout_exercises'
        verbose_name = 'Workout Exercise'
        verbose_name_plural = 'Workouts Exercises'
        default_related_name = 'workout_exercises'


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
    exercise_name = models.CharField(max_length=255, null=True, blank=True)
    weight_in_kg = models.IntegerField(null=True)
    rest_period = models.IntegerField(null=True)
    # rest_period = models.DurationField(null=True)

    class Meta:
        db_table = 'workout_history_exercises'
        verbose_name = 'Workout History Exercise'
        verbose_name_plural = 'Workout History Exercises'
        default_related_name = 'workout_history_exercises'

    # class GymMember(BaseModel):
    ...

    # class GymInstructor(BaseModel):
    ...
    # user = models.ForeignKey(
    #     'users.Users',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    # )
    # gym = models.ForeignKey(
    #     'users.Gym',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    # )
    # instructor_type = models.CharField(max_length=255)

    # class Meta:
    #
