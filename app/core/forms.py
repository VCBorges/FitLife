from django import forms

from app.core import formsmixins as mixins


class BaseForm(
    mixins.BaseFormMixin,
    forms.Form,
):
    def save(self, *args, **kwargs):
        raise NotImplementedError


class BaseUpdateForm(
    mixins.BaseUpdateFormMixin,
    forms.Form,
):
    def save(self, *args, **kwargs):
        raise NotImplementedError
