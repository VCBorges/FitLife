from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.core.utils import default_translation
from apps.gym.validators import translated_field_validator
from apps.users.models import Users

if TYPE_CHECKING:
    from apps.gym.typed import TranslationsSchema


class MuscleGroup(BaseModel):
    name: TranslationsSchema = models.JSONField(
        _('name'),
        validators=[translated_field_validator],
        default=default_translation,
    )
    description: TranslationsSchema = models.JSONField(
        _('description'),
        validators=[translated_field_validator],
        default=default_translation,
    )

    class Meta:
        db_table = 'muscle_groups'
        verbose_name = 'Muscle Group'
        verbose_name_plural = 'Muscle Groups'
        default_related_name = 'muscle_groups'

    REPR_FIELDS = ['name']


class Equipment(BaseModel):
    name: TranslationsSchema = models.JSONField(
        _('name'),
        validators=[translated_field_validator],
        default=default_translation,
    )
    description: TranslationsSchema = models.JSONField(
        _('description'),
        validators=[translated_field_validator],
        default=default_translation,
    )

    class Meta:
        db_table = 'equipments'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
        default_related_name = 'equipments'

    REPR_FIELDS = ['name']


class Exercise(BaseModel):
    name: TranslationsSchema = models.JSONField(
        _('name'),
        validators=[translated_field_validator],
        default=default_translation,
    )
    description: TranslationsSchema = models.JSONField(
        _('description'),
        validators=[translated_field_validator],
        default=default_translation,
    )
    primary_muscle = models.ForeignKey(
        'gym.MuscleGroup',
        verbose_name=_('primary muscle'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_muscle_group',
    )
    secondary_muscle = models.ForeignKey(
        'gym.MuscleGroup',
        verbose_name=_('secondary muscle'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secondary_muscle_group',
    )
    equipment = models.ForeignKey(
        'gym.Equipment',
        verbose_name=_('equipment'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'exercises'
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
        default_related_name = 'exercises'

    REPR_FIELDS = ['name']


class Workout(BaseModel):
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
        null=True,  # TODO: Cannot be null
        blank=True,  # TODO: Cannot be blank
        related_name='creator',
    )

    class Meta:
        db_table = 'workouts'
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'
        default_related_name = 'workouts'

    REPR_FIELDS = ['title']

    @property
    def workout_exercises(self) -> models.BaseManager[WorkoutExercise]:
        return self.workout_exercises


class WorkoutExercise(BaseModel):
    user: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.SET_NULL,
        null=True,
    )
    workout: Workout = models.ForeignKey(
        'gym.Workout',
        verbose_name=_('workout'),
        on_delete=models.SET_NULL,
        null=True,
        editable=True,
    )
    exercise: Exercise = models.ForeignKey(
        'gym.Exercise',
        verbose_name=_('exercise'),
        on_delete=models.SET_NULL,
        null=True,
        editable=True,
    )
    notes = models.TextField(_('notes'), null=True, blank=True)  # ruff: noqa
    repetitions = models.PositiveIntegerField(_('repetitions'), null=True, default=0)
    sets = models.PositiveIntegerField(_('sets'), null=True, default=0)  # series
    weight = models.IntegerField(_('weight'), null=True, default=0)
    rest_period = models.IntegerField(_('rest period'), null=True, default=0)

    class Meta:
        db_table = 'workout_exercises'
        verbose_name = 'Workout Exercise'
        verbose_name_plural = 'Workouts Exercises'
        default_related_name = 'workout_exercises'


class WorkoutExerciseSets(BaseModel):
    user: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.SET_NULL,
        null=True,
    )
    workout_exercise: WorkoutExercise = models.ForeignKey(
        'gym.WorkoutExercise',
        verbose_name=_('workout exercise'),
        on_delete=models.SET_NULL,
        null=True,
    )
    repetitions = models.PositiveIntegerField(_('repetitions'), null=True, default=0)
    weight = models.PositiveIntegerField(_('weight'), null=True, default=0)

    class Meta:
        db_table = 'workout_exercise_sets'
        verbose_name = 'Workout Exercise Set'
        verbose_name_plural = 'Workout Exercise Sets'
        default_related_name = 'workout_exercise_sets'


# TODO: Fix the plural name to <Histories>
class WorkoutHistory(BaseModel):
    user: Users = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        help_text=_('The user who the completed workout'),
    )
    workout: Workout = models.ForeignKey(
        'gym.Workout',
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
        help_text=_('The user who created the completed workout'),
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


class WorkoutHistoryExercises(BaseModel):
    workout_history: WorkoutHistory = models.ForeignKey(
        'gym.WorkoutHistory',
        verbose_name=_('workout history'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exercise: Exercise = models.ForeignKey(
        'gym.Exercise',
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
    is_done = models.BooleanField(_('is completed'), default=False)
    repetitions = models.PositiveIntegerField(_('repetitions'), null=True)
    sets = models.PositiveIntegerField(_('sets'), null=True, default=0)  # series
    weight = models.IntegerField(_('weight'), null=True, default=0)
    rest_period = models.IntegerField(_('rest period'), null=True, default=0)

    class Meta:
        db_table = 'workout_history_exercises'
        verbose_name = 'Workout History Exercise'
        verbose_name_plural = 'Workout History Exercises'
        default_related_name = 'workout_history_exercises'


class WorkoutHistorySets(BaseModel):
    user = models.ForeignKey(
        'users.Users',
        verbose_name=_('user'),
        on_delete=models.SET_NULL,
        null=True,
    )
    workout_history_exercise = models.ForeignKey(
        'gym.WorkoutHistoryExercises',
        verbose_name=_('workout history exercise'),
        on_delete=models.SET_NULL,
        null=True,
    )
    repetitions = models.PositiveIntegerField(_('repetitions'), null=True, default=0)
    weight = models.PositiveIntegerField(_('weight'), null=True, default=0)
    is_done = models.BooleanField(_('is completed'), default=False)

    class Meta:
        db_table = 'workout_history_sets'
        verbose_name = 'Workout History Set'
        verbose_name_plural = 'Workout History Sets'
        default_related_name = 'workout_history_sets'
