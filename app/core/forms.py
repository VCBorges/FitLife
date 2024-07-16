from django import forms

from app.core.mixins import forms as mixins
from app.core.types import ModelType


class BaseForm(
    mixins.BaseFormMixin,
    forms.Form,
):
    def save(self, *args, **kwargs):
        raise NotImplementedError


class BaseInstanceForm(
    mixins.BaseInstanceFormMixin[ModelType],
    forms.Form,
):
    def save(self, *args, **kwargs):
        raise NotImplementedError
