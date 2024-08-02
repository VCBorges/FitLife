from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.core.models import BaseModel
from src.users.models import Users


class MuscleGroups(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True)  # ruff: noqa

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
        verbose_name=_('primary muscle'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_muscle_group',
    )
    secondary_muscle = models.ForeignKey(
        'gym.MuscleGroups',
        verbose_name=_('secondary muscle'),
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
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa
    user: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_by: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('created by'),
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
    def workout_exercises(self) -> models.QuerySet[WorkoutExercises]:
        return self.workout_exercises


# TODO: Fix the plural name to <Histories>
class WorkoutHistory(BaseModel):
    user: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    workout: Workouts = models.ForeignKey(
        'gym.Workouts',
        verbose_name=_('workout'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_by: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('created by'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='history_created_by',
    )
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

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
    user: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.SET_NULL,
        null=True,
    )
    workout: Workouts = models.ForeignKey(
        'gym.Workouts',
        verbose_name=_('workout'),
        on_delete=models.SET_NULL,
        null=True,
    )
    exercise: Exercises = models.ForeignKey(
        'gym.Exercises',
        verbose_name=_('exercise'),
        on_delete=models.SET_NULL,
        null=True,
    )
    repetitions = models.PositiveIntegerField(_('repetitions'), null=True)
    sets = models.PositiveIntegerField(_('sets'), null=True)  # series
    weight = models.IntegerField(_('weight'), null=True)
    rest_period = models.IntegerField(_('rest period'), null=True)

    class Meta:
        db_table = 'workout_exercises'
        verbose_name = 'Workout Exercise'
        verbose_name_plural = 'Workouts Exercises'
        default_related_name = 'workout_exercises'


class WorkoutHistoryExercises(BaseModel):
    workout_history: WorkoutHistory = models.ForeignKey(
        'gym.WorkoutHistory',
        verbose_name=_('workout history'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exercise: Exercises = models.ForeignKey(
        'gym.Exercises',
        verbose_name=_('exercise'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    repetitions = models.PositiveIntegerField(_('repetitions'), null=True)
    sets = models.PositiveIntegerField(_('sets'), null=True)  # series
    name = models.CharField(_('name'), max_length=255, null=True, blank=True)
    weight = models.IntegerField(_('weight'), null=True)
    rest_period = models.IntegerField(_('rest period'), null=True)

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
