from typing import TypeVar

from django.db import models
from django.db.models import F

Model = TypeVar('Model', bound=models.Model)


def get_model_select_field_options(
    *,
    model: Model,
    value_field: str = 'uuid',
    label_field: str = 'name',
    **lookup_filters,
) -> list[Model]:
    return list(
        model.objects.filter(**lookup_filters).values(
            value=F(value_field),
            label=F(label_field),
        )
    )
