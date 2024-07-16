from dataclasses import dataclass

from django.db.models import QuerySet

from app.core.repositories import BaseRepository
from app.users import models
from app.users.transfer import CreateUserDTO, UpdateUserDTO


@dataclass
class UsersRepository(
    BaseRepository[
        models.Users,
        CreateUserDTO,
        UpdateUserDTO,
    ]
):
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
    def filter_by_email(email: str) -> QuerySet[models.Users]:
        return models.Users.objects.filter(email=email)
