# TODO: Change DTO`s to receive models inatnces to clone instead of field values
from typing import ClassVar

from django.db.models import QuerySet

from app.core.repositories import BaseRepository
from app.core.utils import db
from app.gym import models
from app.gym.transfer.workouts import (
    WorkoutsHistoryCreateDTO,
    WorkoutsHistoryExercisesCreateDTO,
    WorkoutsHistoryExercisesUpdateDTO,
)
from app.users.models import Users


class WorkoutsHistoryRepository(
    BaseRepository[
        models.WorkoutHistory,
        WorkoutsHistoryCreateDTO,
        WorkoutsHistoryExercisesUpdateDTO,
    ]
):
    model_class: ClassVar[models.WorkoutHistory] = models.WorkoutHistory
    create_dto: ClassVar[WorkoutsHistoryCreateDTO] = WorkoutsHistoryCreateDTO

    @classmethod
    def filter_by_user(
        cls,
        user: Users,
        prefetch_related: list[str] = None,
        select_related: list[str] = None,
        **lookup_filters,
    ) -> QuerySet[models.WorkoutHistory]:
        queryset = cls.model_class.objects.filter(
            user=user,
            **lookup_filters,
        )
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        if select_related:
            queryset = queryset.select_related(*select_related)
        return queryset

    @staticmethod
    def get_exercises(
        workout_history: models.WorkoutHistory,
    ) -> QuerySet[models.WorkoutHistoryExercises]:
        return models.WorkoutHistoryExercises.objects.filter(
            workout_history=workout_history
        )

    @staticmethod
    def create_exercise(
        *,
        workout_history: models.WorkoutHistory,
        dto: WorkoutsHistoryExercisesCreateDTO,
    ) -> models.WorkoutHistoryExercises:
        return db.create(
            model=models.WorkoutHistoryExercises,
            dto=dto,
            workout_history=workout_history,
        )

    @staticmethod
    def bulk_create_exercises(
        *,
        workout_history: models.WorkoutHistory,
        exercises: list[WorkoutsHistoryExercisesCreateDTO],
    ) -> list[models.WorkoutHistoryExercises]:
        return db.bulk_create(
            model=models.WorkoutHistoryExercises,
            dtos=exercises,
            workout_history=workout_history,
        )

    @staticmethod
    def bulk_delete_exercises(
        *,
        workout_history: models.WorkoutHistory,
        exercises: list[models.WorkoutHistoryExercises],
    ) -> None:
        db.bulk_delete(
            model=models.WorkoutHistoryExercises,
            instances=exercises,
            workout_history=workout_history,
        )
