from typing import Generic, Type

from app.core.types import CreateDTOType, ModelType, UpdateDTOType
from app.core.utils import db


class BaseRepository(Generic[ModelType, CreateDTOType, UpdateDTOType]):
    model_class: Type[ModelType]

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} model_class={self.model_class}>'

    @classmethod
    def get_by_id(cls, id: int) -> ModelType:
        return db.get_by_id(
            model=cls.model_class,
            id=id,
        )

    @classmethod
    def get_by_uuid(cls, uuid: str) -> ModelType:
        return db.get_by_uuid(
            model=cls.model_class,
            uuid=uuid,
        )

    @classmethod
    def get_by_uuid_or_400(cls, uuid: str) -> ModelType:
        return db.get_by_uuid_or_400(
            cls.model_class,
            uuid=uuid,
        )

    @classmethod
    def create(cls, dto: CreateDTOType) -> ModelType:
        return db.create(model=cls.model_class, dto=dto)

    @staticmethod
    def update(
        dto: UpdateDTOType,
    ) -> None:
        db.update(dto)

    @staticmethod
    def delete(instance: ModelType) -> None:
        instance.delete()
