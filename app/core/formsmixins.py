from typing import Callable, TypeVar

from django.db import models
from django.http import HttpRequest

from app.core.protocols import AuthenticatedRequest

T = TypeVar('T', bound=models.Model)


class BaseFormMixin:
    def __init__(
        self, request: HttpRequest | AuthenticatedRequest, *args, **kwargs
    ) -> None:
        self.request = request
        super().__init__(*args, **kwargs)


class BaseUpdateFormMixin(BaseFormMixin):
    get_or_404_fn: Callable[[str], T]

    def __init__(
        self,
        pk: str,
        *args,
        **kwargs,
    ) -> None:
        if not self.get_or_404_fn:
            raise ValueError('get_or_404_fn is required')
        self.instance = self.get_or_404_fn(pk)
        super().__init__(*args, **kwargs)
