from typing import TypedDict

from app.gym import models
from app.gym.repositories.workouts import (
    WorkoutExerciseCreateDTO,
    WorkoutExerciseUpdateDTO,
)


class UpdateWorkoutExercisesDict(TypedDict, total=False):
    create: list[WorkoutExerciseCreateDTO]
    update: list[tuple[models.WorkoutExercises, WorkoutExerciseUpdateDTO]]
    delete: list[models.WorkoutExercises]
