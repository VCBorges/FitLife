from typing import Any

from django.http.request import HttpRequest


class BaseFormMixin:
    def __init__(self, *args, **kwargs):
        self.request: HttpRequest = kwargs.pop('request', None)
        self.context: dict[str, Any] = kwargs.pop('context', None)
        super().__init__(*args, **kwargs)
