from django.test import Client

from app.gym.services import workouts as ws
from app.users.models import Users
from app.users.repositories.users import CreateUserDTO
from app.users.services.users import create_user
from tests.gym import factories

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


@pytest.fixture
def mock_user() -> Users:
    user = create_user(
        email='test@test.com',
        password='testpassword',
        first_name='test',
        last_name='test',
        birth_date='1990-01-01',
        document='77091167015',
    )
    return user


@pytest.fixture
def authenticated_user(client: Client):
    """Fixture to create an authenticated user."""
    user = create_user(
        email='test@test.com',
        password='testpassword',
        first_name='test',
        last_name='test',
        birth_date='1990-01-01',
        document='77091167015',
    )
    client.login(username='test@test.com', password='testpassword')
    return user


@pytest.fixture
def mock_workout(mock_user: Users):
    return ws.create_workout(
        user=mock_user,
        title='Test Workout',
        description='Test Workout Description',
    )


@pytest.fixture
def mock_workout_with_exercise(mock_user: Users):
    ex1 = factories.ExercisesFactory()

    workout = ws.create_workout(
        user=mock_user,
        title='Test Workout',
        description='Test Workout Description',
        exercises=[
            ws.WorkoutExerciseCreateDTO(
                exercise=ex1,
                repetitions=10,
                sets=3,
            ),
        ],
    )
    workout.refresh_from_db()
    return workout


# def mock_nested_form_field_form()
