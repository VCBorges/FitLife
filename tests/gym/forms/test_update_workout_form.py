from app.gym import models
from app.gym.forms import UpdateWorkoutForm
from tests.gym import factories

import pytest


@pytest.mark.django_db
def test_to_be_valid_with_empty_exercises():
    workout = factories.WorkoutsFactory()
    form = UpdateWorkoutForm(
        data={
            'name': 'fdsf',
            'description': 'dsfdsf',
            'exercises': {},
        },
        uuid=workout.uuid,
        request=None,
    )
    assert form.is_valid() is True


@pytest.mark.django_db
def test_self_instance_to_be_a_workout():
    workout = factories.WorkoutsFactory()
    form = UpdateWorkoutForm(
        data={
            'name': 'fdsf',
            'description': 'dsfdsf',
            'exercises': {},
        },
        uuid=workout.uuid,
        request=None,
    )
    assert isinstance(form.instance, models.Workouts)
    assert form.instance.uuid == workout.uuid


@pytest.mark.django_db
def test_save_to_update_workout():
    workout: models.Workouts = factories.WorkoutsFactory()
    new_name = 'fsdfsd'
    new_description = 'dsadsfd'

    form = UpdateWorkoutForm(
        data={
            'name': new_name,
            'description': new_description,
            'exercises': {},
        },
        uuid=workout.uuid,
        request=None,
    )
    form.is_valid()
    print(f'{form.cleaned_data = }')
    form.save()
    workout.refresh_from_db()

    assert workout.title == new_name
    assert workout.description == new_description
