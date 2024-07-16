from typing import Generic

from django.http import HttpRequest

from app.core.protocols import AuthenticatedRequest
from app.core.types import ModelType
from app.core.utils.db import get_by_uuid_or_400


class BaseFormMixin:
    def __init__(
        self, request: HttpRequest | AuthenticatedRequest | None = None, *args, **kwargs
    ) -> None:
        self.request = request
        super().__init__(*args, **kwargs)


# TODO: Customize the message when the instance is not found
class BaseInstanceFormMixin(BaseFormMixin, Generic[ModelType]):
    model_class: type[ModelType]

    def __init__(
        self,
        uuid: str,
        *args,
        **kwargs,
    ) -> None:
        self.instance: ModelType = get_by_uuid_or_400(
            model=self.model_class,
            uuid=uuid,
        )
        super().__init__(*args, **kwargs)
