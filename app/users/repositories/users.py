from dataclasses import dataclass

from django.db.models import QuerySet

from app.core.repositories import BaseDTO, BaseRepository
from app.users import models


@dataclass
class CreateUserDTO(BaseDTO):
    email: str
    password: str
    first_name: str
    last_name: str
    birth_date: str
    document: str


@dataclass
class UsersRepository(BaseRepository):
    @staticmethod
    def get_by_id(id: int) -> models.Users:
        return models.Users.objects.get(pk=id)

    @staticmethod
    def get_by_uuid(uuid: str) -> models.Users:
        return models.Users.objects.get(uuid=uuid)

    @staticmethod
    def get_by_email(email: str) -> models.Users:
        return models.Users.objects.get(email=email)

    @staticmethod
    def create(
        *,
        dto: CreateUserDTO,
    ) -> models.Users:
        return models.Users.objects.create_user(
            **dto.to_dict(),
        )

    @staticmethod
    def update(
        instance: models.Users,
        *,
        dto: BaseDTO,
    ) -> None:
        instance(**dto.to_dict())

    @staticmethod
    def delete(instance: models.Users) -> None:
        instance.delete()

    @staticmethod
    def filter_by_email(email: str) -> QuerySet[models.Users]:
        return models.Users.objects.filter(email=email)
