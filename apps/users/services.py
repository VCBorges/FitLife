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

    def update_user(self, user_data):
        ...

    def unactivate_user(self, user: Users) -> None:
        user.is_active = False
        user.save()

    def confirm_email(self, user: Users) -> None:
        ...

    def reset_password(self, user: Users) -> None:
        ...

    def change_email(self, user: Users) -> None:
        ...

    def change_password(self, user: Users) -> None:
        ...
