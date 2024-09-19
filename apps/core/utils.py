from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from apps.core.exceptions import ObjectDoesNotExist

if TYPE_CHECKING:
    from apps.core import typed
    from apps.gym.typed import TranslationsSchema


def get_or_404(
    *,
    model: type[typed.DjangoModelType],
    pk: str,
    message: str | None = None,
    **lookup_filters,
) -> typed.DjangoModelType:
    try:
        return model.objects.get(
            pk=pk,
            **lookup_filters,
        )
    except model.DoesNotExist:
        if not message:
            message = f'{model.__name__} with id {pk} not found'
        raise ObjectDoesNotExist(message)


def set_model_fields(
    model: typed.DjangoModelType,
    data: dict[str, Any],
) -> None:
    for key, value in data.items():
        setattr(model, key, value)


def default_translation() -> TranslationsSchema:
    return {
        'en': '',
        'pt': '',
    }


# TODO: To put it into a try-except block and raise the proper exception
def clean_models(*models: typed.DjangoModelType) -> None:
    for model in models:
        model.full_clean()


class BaseDTO:
    def to_dict(self) -> dict[str, Any]:
        return {
            key: value for key, value in asdict(self).items() if value is not None
        }  # ftm: skip
