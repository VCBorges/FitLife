from django.db import transaction

from app.gym import models
from app.gym.repositories.workout_history import (
    WorkoutsHistoryCreateDTO,
    WorkoutsHistoryExercisesCreateDTO,
    WorkoutsHistoryRepository,
)
from app.gym.repositories.workouts import (
    WorkoutCreateDTO,
    WorkoutExerciseCreateDTO,
    WorkoutsRepository,
    WorkoutUpdateDTO,
)
from app.gym.types import UpdateWorkoutExercisesDict
from app.users.models import Users


def create_workout(
    *,
    user: Users,
    title: str,
    description: str | None = None,
    exercises: list[WorkoutExerciseCreateDTO] | None = None,
) -> models.Workouts:
    with transaction.atomic():
        workout = WorkoutsRepository.create(
            WorkoutCreateDTO(
                user=user,
                title=title,
                description=description,
            )
        )
        if exercises:
            WorkoutsRepository.bulk_create_exercises(
                workout=workout,
                exercises=exercises,
            )
        return workout


def update_workout(
    *,
    workout: models.Workouts,
    name: str | None = None,
    description: str | None = None,
    exercises: UpdateWorkoutExercisesDict | None = None,
) -> None:
    with transaction.atomic():
        WorkoutsRepository.update(
            WorkoutUpdateDTO(
                instance=workout,
                title=name,
                description=description,
            ),
        )

        if not exercises:
            return

        if 'create' in exercises:
            WorkoutsRepository.bulk_create_exercises(
                workout=workout,
                exercises=exercises['create'],
            )
        if 'update' in exercises:
            WorkoutsRepository.bulk_update_exercises(
                exercises=exercises['update'],
            )
        if 'delete' in exercises:
            WorkoutsRepository.bulk_delete_exercises(
                exercises=exercises['delete'],
            )


def delete_workout(workout: models.Workouts) -> None:
    with transaction.atomic():
        workout_exercises = workout.exercises.all()
        workout_exercises.delete()
        workout.delete()


def complete_workout(
    workout: models.Workouts,
) -> models.WorkoutHistory:
    with transaction.atomic():
        workout_history = WorkoutsHistoryRepository.create(
            WorkoutsHistoryCreateDTO(workout=workout)
        )
        workout_exercises = workout.exercises.all()
        workout_history_exercises = [
            WorkoutsHistoryExercisesCreateDTO(workout_exercise=exercise)
            for exercise in workout_exercises
        ]
        WorkoutsHistoryRepository.bulk_create_exercises(
            workout_history=workout_history,
            exercises=workout_history_exercises,
        )
    return workout_history


def uncomplete_workout(
    workout_history: models.WorkoutHistory,
) -> None:
    with transaction.atomic():
        exercises = workout_history.exercises.all()
        WorkoutsHistoryRepository.bulk_delete_exercises(
            workout_history=workout_history,
            exercises=exercises,
        )
        workout_history.delete()
