from src.core.exceptions import ProcessingError
from src.core.typed import ModelType


def get_or_404(
    model: type[ModelType],
    pk: str,
    message: str = 'Instance not found',
    **lookup_filters,
) -> ModelType:
    try:
        return model.objects.get(
            pk=pk,
            **lookup_filters,
        )
    except model.DoesNotExist:
        raise ProcessingError(
            message,
            status_code=404,
        )
