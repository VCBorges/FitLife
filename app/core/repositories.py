from abc import ABC, abstractmethod, abstractstaticmethod
from dataclasses import asdict, astuple, dataclass, fields
from typing import TypeVar

from django.db import models

from app.core.utils.common import remove_dict_none_values

T = TypeVar('T', bound=models.Model)


@dataclass
class BaseDTO:
    def to_dict(self):
        return remove_dict_none_values(asdict(self))

    def to_tuple(self):
        return tuple(filter(lambda x: x is not None), astuple(self))

    @classmethod
    def get_field_names(cls) -> tuple[str]:
        """Return a tuple with all the field names of the dataclass.

        Returns:
            tuple: A tuple containing all the field names.
        """
        return tuple(field.name for field in fields(cls))


class BaseRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_by_id(id: int) -> T:
        pass

    @staticmethod
    @abstractmethod
    def get_by_uuid(uuid: str) -> T:
        pass

    @staticmethod
    @abstractmethod
    def create(**kwargs) -> T:
        pass

    @staticmethod
    @abstractmethod
    def update(instance: int, **kwargs) -> None:
        pass

    @staticmethod
    @abstractmethod
    def delete(self, instance: T) -> None:
        pass
