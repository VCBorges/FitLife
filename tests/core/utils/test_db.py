from app.core.utils import db
from app.gym import models
from app.gym.repositories.workouts import WorkoutCreateDTO, WorkoutUpdateDTO
from tests.gym.factories import WorkoutsFactory
from tests.users.factories import UsersFactory

import pytest


@pytest.mark.django_db
def test_create_to_create_a_instance():
    user = UsersFactory.create()
    dto = WorkoutCreateDTO(
        user=user,
        title='dsads',
        description='dsdfdsf',
    )

    instance = db.create(
        model=models.Workouts,
        dto=dto,
    )

    assert instance


@pytest.mark.django_db
def test_update_to_update_instance():
    workout: models.Workouts = WorkoutsFactory.create()
    new_name = 'dfdsfdsf'
    dto = WorkoutUpdateDTO(instance=workout, title=new_name)

    db.update(dto)
    workout.refresh_from_db()

    assert workout.title == new_name


@pytest.mark.django_db
def test_bulk_create_to_create_instances():
    user = UsersFactory.create()
    dto = WorkoutCreateDTO(
        user=user,
        title='dsads',
        description='dsdfdsf',
    )

    instances = db.bulk_create(
        model=models.Workouts,
        dtos=[dto],
    )

    assert len(instances) == 1
    assert instances[0].title == dto.title
    assert instances[0].description == dto.description


@pytest.mark.django_db
def test_bulk_update_to_update_instances():
    workout: models.Workouts = WorkoutsFactory.create()
    dto = WorkoutUpdateDTO(instance=workout, title='new_name')

    db.bulk_update(
        model=models.Workouts,
        dtos=[dto],
    )

    assert workout.title == dto.title
