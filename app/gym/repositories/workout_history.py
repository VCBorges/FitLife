from datetime import datetime

from django.db.models import QuerySet

from app.core.repositories import BaseRepository
from app.gym import models


class WorkoutsHistoryRepository(BaseRepository):
    @staticmethod
    def get_by_id(id: int) -> models.Workouts:
        return models.WorkoutHistory.objects.get(pk=id)

    @staticmethod
    def get_by_uuid(uuid: str) -> models.Workouts:
        return models.WorkoutHistory.objects.get(uuid=uuid)

    @classmethod
    def create(
        cls,
        *,
        workout: models.Workouts,
        exercises: list[models.WorkoutExercises],
        finished_at: datetime,
    ) -> models.WorkoutHistory:
        workout_history = models.WorkoutHistory(
            workout=workout,
            finished_at=finished_at,
            name=workout.name,
            description=workout.description,
        )
        workout_history.save()
        exercises = [
            cls.create_exercise(
                workout_history=workout_history,
                exercise=exercise,
            )
            for exercise in exercises
        ]
        models.WorkoutHistoryExercises.objects.bulk_create(exercises)
        return workout_history

    @staticmethod
    def update(
        instance: models.WorkoutHistory,
        **kwargs,
    ) -> None:
        for key, value in kwargs.items():
            setattr(instance, key, value)

    @staticmethod
    def delete(instance: models.WorkoutHistory) -> None:
        instance.delete()

    @staticmethod
    def get_exercises(
        workout_history: models.WorkoutHistory,
    ) -> QuerySet[models.WorkoutHistoryExercises]:
        return models.WorkoutHistoryExercises.objects.filter(
            workout_history=workout_history
        )

    @staticmethod
    def _get_exercise_by_uuid(
        *,
        workout: models.Workouts,
        exercise_uuid: str,
    ) -> models.WorkoutHistoryExercises:
        return models.WorkoutHistoryExercises.objects.get(
            workout=workout,
            uuid=exercise_uuid,
        )

    @staticmethod
    def create_exercise(
        *,
        workout_history: models.Workouts,
        exercise: models.WorkoutExercises,
    ) -> models.WorkoutHistoryExercises:
        return models.WorkoutHistoryExercises(
            workout_history=workout_history,
            exercise=exercise.exercise,
            repetitions=exercise.repetitions,
            sets=exercise.sets,
            rest_period=exercise.rest_period,
        )
