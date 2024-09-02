from django.db.models import CharField, F, QuerySet
from django.db.models.functions import Cast


def model_select_input_options(
    *,
    queryset: QuerySet,
    value_field: str,
    text_field: str,
    lookups: dict[str, str] = {},
    order_by: list[str] | None = None,
) -> list[dict[str, str]]:
    queryset = queryset.filter(**lookups)
    queryset = queryset.annotate(
        value_str=Cast(
            F(value_field),
            output_field=CharField(),
        ),
    ).values(
        value=F('value_str'),
        text=F(text_field),
    )
    if order_by:
        queryset = queryset.order_by(*order_by)
    return list(queryset)
