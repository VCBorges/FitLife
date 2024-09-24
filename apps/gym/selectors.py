from dataclasses import dataclass
from typing import Any

from django.core.paginator import Paginator
from django.db.models import F, Prefetch

from apps.core.constants import Language
from apps.core.utils import BaseDTO
from apps.gym import models, typed


@dataclass
class ListExercisesLookups(BaseDTO):
    name: str | None = None
    primary_muscle: models.MuscleGroups | None = None
    equipment: models.Equipments | None = None


def list_exercises(
    *,
    language: Language = Language.EN,
    lookups: ListExercisesLookups | None = None,
    order_by: list[str] | None = None,
) -> list[dict[str, str]]:
    fields = [
        'id',
        'name',
        'muscle',
    ]
    queryset = models.Exercises.objects.values(
        'id'
    )  # This is necessary for renaming result fields that have the same name of moodel fields
    queryset = queryset.annotate(
        name=F(f'name__{language}'),
        muscle=F(f'primary_muscle__name__{language}'),
        muscle_id=F('primary_muscle__id'),
    )
    queryset = queryset.values(*fields)
    if lookups:
        queryset = queryset.filter(**lookups.as_dict())

    if order_by:
        queryset = queryset.order_by(*order_by)
    return list(queryset)


@dataclass
class ListMusclesLookups(BaseDTO):
    name: str | None = None


def list_muscles(
    *,
    language: Language = Language.EN,
    lookups: ListMusclesLookups | None = None,
    order_by: list[str] | None = None,
) -> list[dict[str, Any]]:
    fields = [
        'id',
        'name',
    ]
    queryset = models.MuscleGroups.objects.values('id')
    queryset = queryset.annotate(
        name=F(f'name__{language}'),
    )
    queryset = queryset.values(*fields)
    if lookups:
        queryset = queryset.filter(**lookups.as_dict())
    if order_by:
        queryset = queryset.order_by(*order_by)
    return list(queryset)


@dataclass
class ListEquipmentsLookups(BaseDTO):
    name: str | None = None


def list_equipments(
    *,
    language: Language = Language.EN,
    lookups: ListEquipmentsLookups | None = None,
    order_by: list[str] | None = None,
) -> list[dict[str, Any]]:
    fields = [
        'id',
        'name',
    ]
    queryset = models.Equipments.objects.values('id')
    queryset = queryset.annotate(
        name=F(f'name__{language}'),
    )
    queryset = queryset.values(*fields)
    if lookups:
        queryset = queryset.filter(**lookups.as_dict())
    if order_by:
        queryset = queryset.order_by(*order_by)
    return list(queryset)


class WorkoutSelector:
    @staticmethod
    def list_workouts_history(
        user: models.Users,
        *,
        page: int = 1,
        per_page: int = 10,
        lookups: typed.ListWorkoutsHistoryLookups = {},
        order_by: list[str] = ['-created_at'],
    ):
        exercises = models.WorkoutHistoryExercises.objects.all()
        workouts = models.WorkoutHistory.objects.prefetch_related(
            Prefetch(
                'workout_history_exercises',
                queryset=exercises,
                to_attr='workout_history_exercises',
            ),
        )
        workouts = workouts.filter(
            user=user,
            **lookups,
        )
        workouts = workouts.order_by(*order_by)
        # workouts = models.WorkoutHistory.objects.filter(
        #     user=user)
        paginator = Paginator(
            object_list=workouts,
            per_page=per_page,
        )
        return paginator.get_page(page).object_list
