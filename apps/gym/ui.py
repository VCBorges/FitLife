from dataclasses import dataclass

from django.db.models import CharField, Value
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Concat

from apps.core.constants import Language
from apps.core.ui import model_select_input_options
from apps.core.utils import BaseLookupDTO
from apps.gym import models


@dataclass(frozen=True)
class ListMusclesLookups(BaseLookupDTO):
    name: str | None = None


def muscles_select_input_options(
    *,
    language: Language = Language.EN,
    lookups: ListMusclesLookups | None = None,
    order_by: list[str] | None = None,
) -> list[dict[str, str]]:
    return model_select_input_options(
        queryset=models.MuscleGroups.objects.all(),
        value_field='id',
        text_field=f'name__{language}',
        lookups=lookups.to_dict() if lookups else {},
        order_by=order_by,
    )


@dataclass(frozen=True)
class ListExercisesLookups(BaseLookupDTO):
    name: str | None = None
    primary_muscle: models.MuscleGroups | None = None
    equipment: models.Equipments | None = None


# TODO: Captalize the first letter of the muscle group name
def exercises_select_input_options(
    *,
    language: Language = Language.EN,
    lookups: ListExercisesLookups | None = None,
    order_by: list[str] | None = None,
) -> list[dict[str, str]]:
    queryset = models.Exercises.objects.annotate(
        name_language=KeyTextTransform(language, 'name'),
        primary_muscle_language=KeyTextTransform(language, 'primary_muscle__name'),
        text_field=Concat(
            'name_language',
            Value(' ('),
            'primary_muscle_language',
            Value(')'),
            output_field=CharField(),
        ),
    )
    return model_select_input_options(
        queryset=queryset,
        value_field='id',
        text_field='text_field',
        lookups=lookups.to_dict() if lookups else {},
        order_by=order_by,
    )
