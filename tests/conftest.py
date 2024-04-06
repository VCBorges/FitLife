from app.users.repositories.users import CreateUserDTO

import pytest


@pytest.fixture
def mock_create_user_dto() -> CreateUserDTO:
    return CreateUserDTO(
        email='test@test.com',
        password='testpassword',
        first_name='test',
        last_name='test',
        birth_date='1990-01-01',
        document='77091167015',
    )
