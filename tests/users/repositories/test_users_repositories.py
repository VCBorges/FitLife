from app.users.repositories.users import CreateUserDTO, UsersRepository

import pytest


@pytest.mark.django_db
def test_create_user_to_have_correct_attrs(mock_create_user_dto: CreateUserDTO):
    dto = mock_create_user_dto
    user = UsersRepository.create(dto=dto)

    assert user.email == dto.email
    assert user.first_name == dto.first_name
    assert user.last_name == dto.last_name
    assert user.birth_date == dto.birth_date
    assert user.document == dto.document
    assert user.is_active is True
