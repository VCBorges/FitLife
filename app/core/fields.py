from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.db import models

from app.core.types import FieldType, FormType, ModelType
from app.core.utils.db import get_by_uuid_or_400


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
            raise forms.ValidationError('Invalid Schema, string expected.')
        return cleaned_data


class NestedFormField(forms.JSONField):
    def __init__(self, form_class: type[FormType], *args, **kwargs):
        self.form_class = form_class
        super().__init__(*args, **kwargs)

    def to_python(self, value: dict[str, Any]) -> dict[str, Any]:
        data = super().to_python(value)
        if data is None:
            return data
        if not isinstance(data, dict):
            raise forms.ValidationError('NestedFormField expects a dict.')
        return data

    def clean(self, value: Any) -> dict[str, Any]:
        cleaned_data = super().clean(value)  # TODO: Check if this is necessary.
        if cleaned_data is None:
            return cleaned_data
        form = self.form_class(
            data=cleaned_data,
            request=None,
        )
        if not form.is_valid():
            raise forms.ValidationError(f'Invalid Schema, {repr(form.errors)}')
        return form.cleaned_data


class ListField(forms.JSONField):
    def __init__(self, *args, **kwargs):
        self.children_field: FieldType = kwargs.pop('children_field')
        if not isinstance(self.children_field, forms.Field):
            raise ValueError('children_field must be a valid Field instance.')
        super().__init__(*args, **kwargs)

    def to_python(self, value: list[Any]) -> list[Any]:
        data = super().to_python(value)
        if data is None:
            return data
        if not isinstance(data, list):
            raise forms.ValidationError('Invalid Schema, list expected.')
        return data

    def clean(self, value: Any) -> list[Any]:
        if value is None:
            return value

        if not isinstance(value, list):
            raise forms.ValidationError('Input must be a list.')

        cleaned_data = []
        errors = []
        for item in value:
            try:
                cleaned_data.append(self.children_field.clean(item))
            except forms.ValidationError:
                errors.append(item)

        if errors:
            raise forms.ValidationError(f'Invalid Schema, {errors} are invalid.')
        return cleaned_data


# TODO: Add support to customize instance not found error message.
class ModelField(forms.UUIDField):
    def __init__(
        self,
        model_class: type[ModelType],
        *args,
        **kwargs,
    ):
        self.model_class = model_class
        if not issubclass(self.model_class, models.Model):
            raise ValueError(
                'model_class must be a subclass of django.db.models.Model.'
            )
        super().__init__(*args, **kwargs)

    def clean(self, value: Any) -> ModelType:
        value = super().clean(value)
        if value is None:
            return value
        instance = get_by_uuid_or_400(
            model=self.model_class,
            uuid=value,
            message=f'{self.model_class.__name__} with uuid {value} does not exist.',
        )
        return instance
