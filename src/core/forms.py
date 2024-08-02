from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from django import forms
from django.http import HttpRequest

from src.core.exceptions import ProcessingError

if TYPE_CHECKING:
    pass


class BaseForm(forms.Form):
    @override
    def __init__(
        self,
        request: HttpRequest | None = None,
        *args,
        **kwargs,
    ) -> None:
        self.request = request
        super().__init__(*args, **kwargs)

    normalized_fields_mapping = {}

    def normalize_cleaned_data(self) -> dict[str, Any]:
        for key, value in self.normalized_fields_mapping.items():
            if key in self.cleaned_data:
                self.cleaned_data[value] = self.cleaned_data.pop(key)

    @override
    def clean(self) -> dict[str, Any]:
        data = super().clean()
        self.normalize_cleaned_data()
        return data

    @override
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if valid:
            return valid

        raise ProcessingError(
            code=400,
            message='Error',
            params={
                'errors': self.errors,
            },
        )
