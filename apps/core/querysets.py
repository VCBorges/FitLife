from apps.core.exceptions import ObjectDoesNotExist
from apps.core.typed import DjangoModelType


def get_or_404(
    *,
    model: type[DjangoModelType],
    pk: str,
    message: str | None = None,
    **lookup_filters,
) -> DjangoModelType:
    try:
        return model.objects.get(
            pk=pk,
            **lookup_filters,
        )
    except model.DoesNotExist:
        if not message:
            message = f'{model.__name__} with id {pk} not found'
        raise ObjectDoesNotExist(message)
