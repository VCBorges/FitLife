from __future__ import annotations

import typing as tp

if tp.TYPE_CHECKING:
    import datetime

    from apps.gym import models


class TranslationsSchema(tp.TypedDict):
    en: str
    pt: str


class CreateWorkoutExerciseSchema(tp.TypedDict):
    exercise: models.Exercise
    sets: int | None
    repetitions: int | None
    weight: float | None
    rest: int | None


class UpdateWorkoutExerciseSchema(tp.TypedDict):
    workout_exercise: models.WorkoutExercise
    exercise: models.Exercise
    sets: int | None
    repetitions: int | None
    weight: float | None
    rest: int | None


class ExercisesUpdateWorkout(tp.TypedDict, total=False):
    to_create: list[CreateWorkoutExerciseSchema]
    to_update: list[models.WorkoutExercise]
    to_delete: list[models.WorkoutExercise]


class ListWorkoutsHistoryLookups(tp.TypedDict, total=False):
    title: str
    description: str
    completed_at: datetime.datetime


class CompleteWorkoutExerciseSchema(tp.TypedDict, total=False):
    workout_exercise: models.WorkoutExercise
    repetitions: int
    sets: int
    weight: int
    rest_period: int
    is_done: bool
