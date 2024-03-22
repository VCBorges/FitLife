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
        workout: models.WorkoutHistory,
    ) -> QuerySet[models.WorkoutHistoryExercises]:
        return models.WorkoutHistoryExercises.objects.filter(workout=workout)

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

    # @classmethod
    # def remove_exercise_by_uuid(
    #     cls,
    #     *,
    #     workout: models.Workouts,
    #     exercise_uuid: str,
    # ) -> None:
    #     workout_exercise = cls._get_exercise_by_uuid(
    #         workout=workout,
    #         exercise_uuid=exercise_uuid,
    #     )
    #     workout_exercise.delete()

    # @classmethod
    # def update_exercise_by_uuid(
    #     cls,
    #     *,
    #     workout: models.Workouts,
    #     exercise_uuid: str,
    #     repetitions: int,
    #     sets: int,
    #     rest_period: int,
    # ) -> models.WorkoutHistoryExercises:
    #     workout_exercise = cls._get_exercise_by_uuid(
    #         workout=workout,
    #         exercise_uuid=exercise_uuid,
    #     )
    #     workout_exercise.repetitions = repetitions
    #     workout_exercise.sets = sets
    #     workout_exercise.rest_period = rest_period
    #     workout_exercise.save()
    #     return workout_exercise
