from typing import TypedDict

from django.db.models import CharField, F, QuerySet
from django.db.models.functions import Cast


class SelectOptionsSchema(TypedDict):
    value: str
    text: str


def model_select_input_options(
    *,
    queryset: QuerySet,
    value_field: str,
    text_field: str,
    extra_fields: list[str] = [],
    extra_expressions: dict[str, F] = {},
) -> list[SelectOptionsSchema]:
    queryset = queryset.annotate(
        value_str=Cast(
            F(value_field),
            output_field=CharField(),
        ),
    ).values(
        value=F('value_str'),
        text=F(text_field),
        *extra_fields,
        **extra_expressions,
    )
    return list(queryset)
