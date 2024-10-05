from __future__ import annotations

import datetime
import typing as tp
from dataclasses import dataclass

from apps.core.utils import BaseDTO

if tp.TYPE_CHECKING:
    from apps.gym import models
    from apps.users.models import Users


@dataclass(frozen=True)
class MusclesLookups(BaseDTO):
    name: str | None = None


@dataclass(frozen=True)
class ExercisesLookups(BaseDTO):
    name: str | None = None
    primary_muscle: models.MuscleGroups | None = None
    equipment: models.Equipments | None = None


@dataclass(frozen=True)
class EquipmentsLookups(BaseDTO):
    name: str | None = None


@dataclass(frozen=True)
class WorkoutLookups(BaseDTO):
    title: str | None = None
    description: str | None = None
    title__icontains: str | None = None


@dataclass(frozen=True, kw_only=True)
class UserWorkoutLookups(WorkoutLookups):
    user: Users


@dataclass(frozen=True, kw_only=True)
class UserWorkoutHistoryLookups(UserWorkoutLookups):
    workout: models.Workouts | None = None
    completed_at: datetime.datetime | None = None
    creator: Users | None = None


# TODO: move to core module
@dataclass(frozen=True)
class PaginatedData(BaseDTO):
    total_pages: int
    current_page: int
    total_size: int
    page_size: int
    data: list[dict[str, tp.Any]]
