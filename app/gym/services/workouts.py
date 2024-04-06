from django import forms

from app.gym import models
from app.gym.repositories.exercises import ExercisesRepository
from app.gym.repositories.workouts import (
    WorkoutExerciseCreateDTO,
    WorkoutExerciseUpdateDTO,
    WorkoutsRepository,
    WorkoutUpdateDTO,
)
from app.users.models import Users


def get_workout_or_404(uuid: str) -> models.Workouts:
    try:
        return WorkoutsRepository.get_by_uuid(uuid)
    except models.Workouts.DoesNotExist:
        raise forms.ValidationError('Workout not found')


def get_workout_exercise_by_uuid_or_404(
    *,
    workout: models.Workouts,
    exercise_uuid: str,
) -> models.WorkoutExercises:
    try:
        return WorkoutsRepository.get_exercise_by_uuid(
            workout=workout,
            exercise_uuid=exercise_uuid,
        )
    except models.WorkoutExercises.DoesNotExist:
        raise forms.ValidationError('Workout exercise not found')


def create_workout(
    *,
    name: str,
    user: Users,
    exercises: list[WorkoutExerciseCreateDTO] | None = None,
    description: str | None = None,
) -> models.Workouts:
    workout = WorkoutsRepository.create(
        name=name,
        user=user,
        description=description,
    )
    workout.save()
    if exercises:
        WorkoutsRepository.bulk_create_exercises(
            workout=workout,
            dtos=exercises,
        )
    return workout


def add_exercises_to_workout(
    *,
    workout: models.Workouts,
    exercises: list[WorkoutExerciseCreateDTO],
) -> models.WorkoutExercises:
    workout_exercises = [
        WorkoutsRepository.create_exercise(
            workout=workout,
            dto=exercise,
        )
        for exercise in exercises
    ]
    models.WorkoutExercises.objects.bulk_create(workout_exercises)
    return workout_exercises


def add_exercise_to_workout(
    *,
    workout: models.Workouts,
    exercise: models.Exercises,
) -> models.WorkoutExercises:
    workout_exercise = WorkoutsRepository.create_exercise(
        workout=workout,
        dto=WorkoutExerciseCreateDTO(
            exercise=exercise,
        ),
    )
    workout_exercise.save()
    return workout_exercise


def update_workout(
    *,
    workout: models.Workouts,
    name: str,
    description: str | None = None,
    excercises: list[tuple[models.WorkoutExercises, WorkoutExerciseUpdateDTO]],
) -> None:
    WorkoutsRepository.update(
        workout,
        dto=WorkoutUpdateDTO(
            name=name,
            description=description,
        ),
    )
    WorkoutsRepository.bulk_update_exercises(excercises)


def validate_workouts_exercises_to_create(
    exercises: list[dict[str, str | int]],
) -> tuple[list[WorkoutExerciseCreateDTO], list[dict[str, str | int]]]:
    exercises_to_create = []
    exercises_with_error = []
    for exercise in exercises:
        try:
            exercises_to_create.append(
                WorkoutExerciseCreateDTO(
                    exercise=ExercisesRepository.get_by_uuid_or_400(
                        exercise['exercise_id']
                    ),
                    sets=exercise['sets'],
                    repetitions=exercise['repetitions'],
                )
            )
        except forms.ValidationError:
            exercises_with_error.append(exercise)
    return (exercises_to_create, exercises_with_error)
