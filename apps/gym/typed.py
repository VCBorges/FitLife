from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from apps.gym import models


class CreateWorkoutExerciseSchema(TypedDict):
    exercise: models.Exercises
    sets: int | None
    repetitions: int | None
    weight: float | None
    rest: int | None


class UpdateWorkoutExerciseSchema(TypedDict):
    workout_exercise: models.WorkoutExercises
    exercise: models.Exercises
    sets: int | None
    repetitions: int | None
    weight: float | None
    rest: int | None


class ExercisesUpdateWorkout(TypedDict, total=False):
    create: list[CreateWorkoutExerciseSchema]
    update: list[models.WorkoutExercises]
    delete: list[models.WorkoutExercises]


class ListWorkoutsHistoryLookups(TypedDict, total=False):
    title: str
    description: str
    completed_at: datetime.datetime


class TranslationsSchema(TypedDict):
    en: str
    pt: str
