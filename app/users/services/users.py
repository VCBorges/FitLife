from app.users.models import Users
from app.users.repositories.users import CreateUserDTO, UsersRepository


def create_user(
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    birth_date: str,
    document: str,
) -> Users:
    dto = CreateUserDTO(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        document=document,
    )
    user = UsersRepository.create(
        dto=dto,
    )
    return user
