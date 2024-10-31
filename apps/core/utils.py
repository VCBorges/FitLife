from __future__ import annotations

import datetime
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils import dateformat

from apps.core.constants import Language
from apps.core.exceptions import ObjectDoesNotExist

if TYPE_CHECKING:
    from apps.core import typed
    from apps.gym.typed import TranslationsSchema


def get_or_404(
    model_or_queryset: typed.DjangoModelType | QuerySet[typed.DjangoModelType],
    *,
    pk: str,
    message: str | None = None,
) -> typed.DjangoModelType:
    if issubclass(model_or_queryset, Model):
        model_or_queryset = model_or_queryset.objects.all()
    try:
        return model_or_queryset.get(pk=pk)
    except model_or_queryset.DoesNotExist:
        if not message:
            message = f'{model_or_queryset.__name__} with id {pk} not found'
        raise ObjectDoesNotExist(message)


def set_model_fields(
    model: typed.DjangoModelType,
    data: dict[str, Any],
) -> None:
    for key, value in data.items():
        setattr(model, key, value)


def default_translation() -> TranslationsSchema:
    return {language.value: '' for language in Language}


# TODO: To put it into a try-except block and raise the proper exception
def clean_models(*models: typed.DjangoModelType) -> None:
    for model in models:
        model.full_clean()


class BaseDTO:
    def as_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
            and value
            not in [
                (None, None),
                (None, None),
            ]
            # and
        }  # ftm: skip


def formatted_date(
    date: datetime.date | datetime.datetime,
    format_string: str | None = None,
) -> str:
    DATE_FORMAT = 'd/m/Y'
    DATETIME_FORMAT = 'd/m/Y H:i'
    if format_string is None:
        if isinstance(date, datetime.datetime):
            format_string = DATETIME_FORMAT
        else:
            format_string = DATE_FORMAT
    return dateformat.format(date, format_string)


def get_tomorrow() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=1)


# def convert_to_local_time(utc_dt: datetime.datetime) -> datetime.datetime:
#     """
#     Convert a UTC datetime to the timezone specified in Django settings.

#     Args:
#         utc_dt (datetime): A datetime object in UTC

#     Returns:
#         datetime: The datetime converted to the local timezone from settings.TIME_ZONE

#     Example:
#         >>> utc_time = datetime.utcnow()
#         >>> local_time = convert_to_local_time(utc_time)
#     """
#     if utc_dt.tzinfo is None:
#         utc_dt = timezone.make_aware(utc_dt, timezone.UTC)

#     return timezone.localtime(
#         utc_dt,
#         timezone=timezone.get_default_timezone()
#     )

# # formatted_date: Callable[[date | datetime], str] = partial(dateformat.format, format_string='d/m/Y H:i')
