from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.core.transfer import BaseDTO, UpdateDTO
from app.gym import models
from app.users.models import Users


@dataclass
class WorkoutCreateDTO(BaseDTO):
    user: Users
    title: str
    description: str | None = None


@dataclass
class WorkoutUpdateDTO(UpdateDTO[models.Workouts]):
    title: str | None = None
    description: str | None = None


@dataclass
class WorkoutExerciseUpdateDTO(UpdateDTO[models.WorkoutExercises]):
    exercise: models.Exercises
    repetitions: int | None = None
    sets: int | None = None
    # rest_period: int | None = None


@dataclass
class WorkoutExerciseCreateDTO(BaseDTO):
    exercise: models.Exercises
    repetitions: int = 0
    sets: int = 0
    weight_in_kg: int | None = None
    rest_period: int = 0


@dataclass
class WorkoutsHistoryCreateDTO(BaseDTO):
    workout: models.Workouts

    completed_at: datetime = field(
        default_factory=datetime.now,
        init=False,
    )
    user: Users = field(init=False)
    title: str = field(init=False)
    description: str | None = field(init=False)

    def __post_init__(self):
        self.user = self.workout.user
        self.title = self.workout.title
        self.description = self.workout.description


@dataclass
class WorkoutsHistoryExercisesCreateDTO(BaseDTO):
    workout_exercise: models.WorkoutExercises

    exercise: models.Exercises = field(init=False)
    repetitions: int = field(init=False)
    sets: int = field(init=False)

    def __post_init__(self):
        self.exercise = self.workout_exercise.exercise
        self.repetitions = self.workout_exercise.repetitions
        self.sets = self.workout_exercise.sets

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data['workout_exercise']
        return data


@dataclass
class WorkoutsHistoryExercisesUpdateDTO(BaseDTO):
    ...
