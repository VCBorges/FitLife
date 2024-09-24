from dataclasses import dataclass
from typing import Any

from apps.core.utils import BaseDTO
from apps.gym import models


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


@dataclass(frozen=True)
class PaginatedData(BaseDTO):
    total_pages: int
    current_page: int
    total_size: int
    page_size: int
    data: list[dict[str, Any]]
