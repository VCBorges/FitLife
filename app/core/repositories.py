from abc import ABC, abstractstaticmethod
from typing import TypeVar

from django.db import models

T = TypeVar('T', bound=models.Model)


class BaseRepository(ABC):
    @abstractstaticmethod
    def get_by_id(id: int) -> T:
        pass

    @abstractstaticmethod
    def get_by_uuid(uuid: str) -> T:
        pass

    @abstractstaticmethod
    def create(**kwargs) -> T:
        pass

    @abstractstaticmethod
    def update(instance: int, **kwargs) -> None:
        pass

    @abstractstaticmethod
    def delete(self, instance: T) -> None:
        pass
