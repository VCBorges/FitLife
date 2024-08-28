from __future__ import annotations

from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.core.utils import default_translation
from apps.users.models import Users


class MuscleGroups(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True)  # ruff: noqa
    translations = models.JSONField(
        _('translation'),
        default=partial(default_translation, 'name', 'description'),
    )

    class Meta:
        db_table = 'muscle_groups'
        verbose_name = 'Muscle Group'
        verbose_name_plural = 'Muscle Groups'
        default_related_name = 'muscle_groups'

    REPR_FIELDS = ['name']


class Equipments(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa
    translations = models.JSONField(
        _('translation'),
        default=partial(default_translation, 'name', 'description'),
    )

    class Meta:
        db_table = 'equipments'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
        default_related_name = 'equipments'

    REPR_FIELDS = ['name']


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
    equipment = models.ForeignKey(
        'gym.Equipments',
        verbose_name=_('equipment'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    translations = models.JSONField(
        _('translation'),
        default=partial(default_translation, 'name', 'description'),
    )

    class Meta:
        db_table = 'exercises'
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
        default_related_name = 'exercises'

    REPR_FIELDS = ['name']

    # def __str__(self):
    #     return f'<{self.__class__.__name__} {self.name}>'


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
    creator: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('creator'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='creator',
    )

    class Meta:
        db_table = 'workouts'
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'
        default_related_name = 'workouts'

    REPR_FIELDS = ['title']

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
    creator: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('creator'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='history_creator',
    )
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)  # ruff: noqa
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    class Meta:
        db_table = 'workout_history'
        verbose_name = 'Workout History'
        verbose_name_plural = 'Workout Historys'
        default_related_name = 'workout_history'

    REPR_FIELDS = [
        'title',
        'completed_at',
    ]

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
