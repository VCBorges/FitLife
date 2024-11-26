from typing import Any

from apps.core.utils import clean_model, set_model_fields
from apps.users.models import Users


class UserService:
    @classmethod
    def create_user(cls, data: dict[str, str]) -> Users:
        user = Users.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
        )
        return user

    def update_user(self, user: Users, data: dict[str, Any]) -> None:
        update_fields = [
            'first_name',
            'last_name',
            'birth_date',
            'height',
            'weight',
        ]
        set_model_fields(
            model=user,
            data=data,
        )
        clean_model(user)
        user.save(update_fields=update_fields)

    def deactivate_user(self, user: Users) -> None:
        user.is_active = False
        user.save()

    def confirm_email(self, user: Users) -> None: ...

    def reset_password(self, user: Users) -> None: ...

    def change_email(self, user: Users) -> None: ...

    def change_password(self, user: Users) -> None: ...
