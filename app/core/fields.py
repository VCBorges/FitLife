from typing import Any, TypeVar

from django import forms
from django.core.exceptions import ValidationError

T = TypeVar('T', bound=forms.Form)
_T = TypeVar('_T', bound=forms.Field)


class StrictCharField(forms.CharField):
    def to_python(self, value: Any):
        if value is None:
            return value
        if isinstance(value, str):
            return value.strip()
        raise ValidationError('This field requires a string input.')

    def clean(self, value: Any) -> str:
        cleaned_data = super().clean(value)
        if not isinstance(cleaned_data, str):
            raise forms.ValidationError('Invalid Schema, string expected.')
        return cleaned_data


class NestedFormField(forms.JSONField):
    def __init__(self, *args, **kwargs):
        self.form_class: type[T] = kwargs.pop('form_class')
        super().__init__(*args, **kwargs)

    def to_python(self, value: dict[str, Any]) -> dict[str, Any]:
        data = super().to_python(value)
        return data

    def clean(self, value: Any) -> dict[str, Any]:
        cleaned_data = super().clean(value)
        form = self.form_class(value)
        if not form.is_valid():
            raise forms.ValidationError(f'Invalid Schema, {form.errors = }')
        return cleaned_data


class ListField(forms.JSONField):
    def __init__(self, *args, **kwargs):
        self.children_field: _T = kwargs.pop('children_field')
        if not isinstance(self.children_field, forms.Field):
            raise ValueError('children_field must be a valid Field instance.')
        super().__init__(*args, **kwargs)

    def to_python(self, value: list[Any]) -> list[Any]:
        data = super().to_python(value)
        if not isinstance(data, list):
            raise forms.ValidationError('Invalid Schema, list expected.')
        return data

    def clean(self, value: Any) -> list[Any]:
        if not isinstance(value, list):
            raise forms.ValidationError('Input must be a list.')

        cleaned_data = []
        for item in value:
            cleaned_data.append(self.children_field.clean(item))
        return cleaned_data
