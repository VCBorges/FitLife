from __future__ import annotations

from typing import Any, override

from django.forms import ValidationError as DjangoValidationError


class BaseError(Exception):
    def __init__(
        self,
        *,
        message: str = '',
        status_code: int = 500,
        data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_dict = data
        self.message = message


class FieldValidationError(DjangoValidationError):
    def __init__(
        self,
        data: str
        | list[Any]
        | dict[str, Any]
        | 'FieldValidationError'
        | DjangoValidationError,
    ) -> None:
        if isinstance(data, FieldValidationError):
            if hasattr(data, 'error_dict'):
                data = data.error_dict
            else:
                data = data.error_list

        elif isinstance(data, DjangoValidationError):
            if hasattr(data, 'error_dict'):
                data = data.message_dict
            else:
                data = data.messages

        if isinstance(data, dict):
            self.error_dict = data

        elif isinstance(data, list):
            self.error_list: list = data

        else:
            self.error_list = [data]

    def __iter__(self):
        if hasattr(self, 'error_dict'):
            for field, errors in self.error_dict.items():
                yield field, errors
        else:
            for error in self.error_list:
                yield error

    def __str__(self):
        if hasattr(self, 'error_dict'):
            return repr(self.error_dict)
        return repr(self.error_list)

    def __repr__(self):
        return f'{self.__class__.__name__}({self})'


class FormValidationError(BaseError):
    MESSAGE = 'Invalid data.'
    STATUS_CODE = 400

    @override
    def __init__(
        self,
        errors: dict[str, Any],
        *,
        message: str | None = None,
    ) -> None:
        super().__init__(
            message=message or self.MESSAGE,
            status_code=self.STATUS_CODE,
            data=errors,
        )


class ObjectDoesNotExist(BaseError):
    MESSAGE = 'Object does not exist.'
    STATUS_CODE = 404

    @override
    def __init__(
        self,
        message: str | None = None,
    ) -> None:
        super().__init__(
            message=message or self.MESSAGE,
            status_code=self.STATUS_CODE,
        )
