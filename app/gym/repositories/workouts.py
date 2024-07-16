from typing import ClassVar, Sequence

from django.db.models import QuerySet

from app.core.repositories import BaseRepository
from app.core.utils import db
from app.gym import models
from app.gym.transfer.workouts import (
    WorkoutCreateDTO,
    WorkoutExerciseCreateDTO,
    WorkoutExerciseUpdateDTO,
    WorkoutUpdateDTO,
)
from app.users.models import Users


class WorkoutsRepository(
    BaseRepository[models.Workouts, WorkoutCreateDTO, WorkoutUpdateDTO]
):
    model_class: ClassVar[models.Workouts] = models.Workouts

    @classmethod
    def filter_by_user(
        cls,
        user: Users,
        prefetch_related: list[str] = None,
        select_related: list[str] = None,
        order_by: list[str] | None = None,
        **lookup_filters,
    ) -> QuerySet[models.Workouts]:
        queryset = cls.model_class.objects.filter(
            user=user,
            **lookup_filters,
        )
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        if select_related:
            queryset = queryset.select_related(*select_related)
        if order_by:
            queryset = queryset.order_by(*order_by)
        return queryset

    @staticmethod
    def filter_exercises(
        workout: models.Workouts,
        *,
        prefetch_related: list[str] = None,
        select_related: list[str] = None,
        **lookup_filters,
    ) -> QuerySet[models.WorkoutExercises]:
        queryset = workout.exercises.filter(**lookup_filters)
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        if select_related:
            queryset = queryset.select_related(*select_related)
        return queryset

    @staticmethod
    def get_exercise_by_uuid(
        *,
        workout: models.Workouts,
        uuid: str,
    ) -> models.WorkoutExercises:
        return db.get_by_uuid(
            model=models.WorkoutExercises,
            uuid=uuid,
            workout=workout,
        )

    @classmethod
    def get_exercise_by_uuid_or_404(
        cls,
        *,
        workout: models.Workouts,
        uuid: str,
    ) -> models.WorkoutExercises:
        return db.get_by_uuid_or_400(
            model=models.WorkoutExercises,
            uuid=uuid,
            workout=workout,
        )

    @staticmethod
    def create_exercise(
        workout: models.Workouts,
        dto: WorkoutExerciseCreateDTO,
    ) -> models.WorkoutExercises:
        return db.create(
            model=models.WorkoutExercises,
            dto=dto,
            workout=workout,
        )

    @classmethod
    def bulk_create_exercises(
        cls,
        workout: models.Workouts,
        exercises: list[WorkoutExerciseCreateDTO],
    ) -> list[models.WorkoutExercises]:
        return db.bulk_create(
            model=models.WorkoutExercises,
            dtos=exercises,
            workout=workout,
        )

    @staticmethod
    def delete_exercise(instance: models.WorkoutExercises) -> None:
        instance.delete()

    @staticmethod
    def update_exercise(
        dto: WorkoutExerciseUpdateDTO,
    ) -> None:
        db.update(dto)

    @staticmethod
    def bulk_update_exercises(
        exercises: list[WorkoutExerciseUpdateDTO],
    ) -> None:
        db.bulk_update(
            model=models.WorkoutExercises,
            dtos=exercises,
        )

    @staticmethod
    def bulk_delete_exercises(
        exercises: Sequence[models.WorkoutExercises],
    ) -> None:
        db.bulk_delete(
            model=models.WorkoutExercises,
            instances=exercises,
        )
