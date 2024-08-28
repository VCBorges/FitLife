from apps.core.exceptions import BaseError
from apps.core.typed import ModelType


def get_or_404(
    model: type[ModelType],
    pk: str,
    message: str | None = None,
    **lookup_filters,
) -> ModelType:
    try:
        return model.objects.get(
            pk=pk,
            **lookup_filters,
        )
    except model.DoesNotExist:
        if not message:
            message = f'{model.__name__} with id {pk} not found'
        raise BaseError(
            message,
            code=404,
        )
