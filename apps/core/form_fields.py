from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorDict, ErrorList

from apps.core.exceptions import FieldValidationError

if TYPE_CHECKING:
    from apps.core.typed import BaseFormType, FieldType


class StrictCharField(forms.CharField):
    def to_python(self, value: Any):
        if value is None:
            return value

        if isinstance(value, str):
            return value.strip()
        raise ValidationError('This field requires a string input.')

    def clean(self, value: Any) -> str:
        cleaned_data = super().clean(value)
        if cleaned_data is None:
            return cleaned_data

        if not isinstance(cleaned_data, str):
            raise forms.ValidationError('String expected.')

        return cleaned_data


class NestedFormField(forms.JSONField):
    empty_values = [None, {}]

    def __init__(self, form_class: type[BaseFormType], *args, **kwargs):
        self.form_class = form_class
        super().__init__(*args, **kwargs)

    def to_python(self, value: dict[str, Any]) -> dict[str, Any]:
        data = super().to_python(value)
        if data in self.empty_values:
            return data

        if not isinstance(data, dict):
            raise forms.ValidationError('Invalid Schema, object expected.')

        return data

    def clean(self, value: Any) -> dict[str, Any]:
        cleaned_data = super().clean(value)  # Necessary for validation.
        if cleaned_data in self.empty_values:
            return cleaned_data

        form = self.form_class(
            data=cleaned_data,
            request=None,
        )
        if not form.is_valid(raise_exception=False):
            raise FieldValidationError(form.errors)

        return form.cleaned_data


class ListField(forms.JSONField):
    empty_values = [None, []]

    def __init__(self, children_field: FieldType, *args, **kwargs):
        self.children_field = children_field
        if not isinstance(self.children_field, forms.Field):
            raise ValueError('children_field must be a valid Field instance.')
        super().__init__(*args, **kwargs)

    def to_python(self, value: list[Any]) -> list[Any]:
        data = super().to_python(value)
        if data in self.empty_values:
            return data

        if not isinstance(data, list):
            raise forms.ValidationError('List expected.')

        return data

    def clean(self, value: Any) -> list[Any]:
        cleaned_data = super().clean(value)
        if cleaned_data in self.empty_values:
            return cleaned_data

        if not isinstance(cleaned_data, list):
            raise forms.ValidationError('Input must be a list.')

        validated_data = []
        errors = []
        for i in range(len(cleaned_data)):
            try:
                validated_data.append(self.children_field.clean(cleaned_data[i]))
            except forms.ValidationError as exc:
                if hasattr(exc, 'error_dict'):
                    error = ErrorDict(exc.error_dict)

                elif hasattr(exc, 'error_list'):
                    error = ErrorList(exc)

                else:
                    error = ErrorList(exc.error_list)

                errors.append({i: error})

        if errors:
            raise FieldValidationError(errors)

        return validated_data
