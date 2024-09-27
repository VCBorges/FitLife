from __future__ import annotations

import typing as tp

from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError as DjangoValidationError
from django.forms import FileField
from django.forms.utils import ErrorDict, ErrorList
from django.http import HttpRequest

from apps.core.exceptions import FieldValidationError, FormValidationError

if tp.TYPE_CHECKING:
    from apps.core.typed import DjangoModelType


# TODO: Remove any renderable feature.
class BaseForm(forms.Form):
    normalized_fields_mapping = {}

    @tp.override
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.request: HttpRequest | None = kwargs.pop('request', None)
        self.instance: DjangoModelType | None = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    def normalize_cleaned_data(self) -> dict[str, tp.Any]:
        for key, value in self.normalized_fields_mapping.items():
            if key in self.cleaned_data:
                self.cleaned_data[value] = self.cleaned_data.pop(key)

    @tp.override
    def clean(self) -> dict[str, tp.Any]:
        data = super().clean()
        self.normalize_cleaned_data()
        return data

    @tp.override
    def is_valid(self, *, raise_exception: bool = True) -> bool:
        valid = super().is_valid()

        if not valid and raise_exception:
            raise FormValidationError(self.errors)

        return valid

    @tp.override
    def _clean_fields(self) -> None:
        for name, bf in self._bound_items():
            field = bf.field
            value = bf.initial if field.disabled else bf.data
            try:
                if isinstance(field, FileField):
                    value = field.clean(value, bf.initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value

            except DjangoValidationError as e:
                self.add_error(name, FieldValidationError(e))

    @tp.override
    def add_error(
        self,
        field: str,
        error: FieldValidationError
        | DjangoValidationError
        | list[tp.Any]
        | dict[str, tp.Any]
        | str,
    ) -> None:
        if not isinstance(error, (FieldValidationError, DjangoValidationError)):
            error = FieldValidationError(error)

        if hasattr(error, 'error_dict'):
            self.handle_error_dict(
                field=field,
                error=error,
            )

        else:
            self.handle_error_list(
                field=field,
                error=error,
            )

    def handle_error_list(
        self,
        field: str,
        error: list[tp.Any],
    ) -> None:
        error = {field or NON_FIELD_ERRORS: error.error_list}
        for field, error_list in error.items():
            if field not in self.errors:
                if field != NON_FIELD_ERRORS and field not in self.fields:
                    raise ValueError(
                        "'%s' has no field named '%s'."
                        % (self.__class__.__name__, field)
                    )
                if field == NON_FIELD_ERRORS:
                    self._errors[field] = self.error_class(
                        error_class='nonfield',
                        renderer=self.renderer,
                    )
                else:
                    self._errors[field] = ErrorList()

            self._errors[field].extend(error_list)
            if field in self.cleaned_data:
                del self.cleaned_data[field]

    def handle_error_dict(
        self,
        field: str,
        error: dict[str, tp.Any],
    ) -> None:
        if field not in self.errors:
            if field != NON_FIELD_ERRORS and field not in self.fields:
                raise ValueError(
                    "'%s' has no field named '%s'." % (self.__class__.__name__, field)
                )

            self._errors[field] = ErrorDict()

        self._errors[field].update(error.error_dict)
        if field in self.cleaned_data:
            del self.cleaned_data[field]

    @tp.override
    def _clean_form(self) -> None:
        try:
            cleaned_data = self.clean()
        except DjangoValidationError as e:
            self.add_error(None, FieldValidationError(e))

        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data
