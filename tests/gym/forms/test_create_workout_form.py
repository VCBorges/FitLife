from app.gym.forms import CreateWorkoutForm
from tests.gym import factories

import pytest


@pytest.mark.django_db
def test_to_be_valid_with_empty_exercises():
    form = CreateWorkoutForm(
        data={
            'title': 'fdsf',
            'description': 'dsfdsf',
            'exercises': [],
        },
        request=None,
    )
    assert form.is_valid() is True


@pytest.mark.django_db
def test_to_be_valid_with_exercises():
    exercises = [
        factories.ExercisesFactory(),
        factories.ExercisesFactory(),
    ]
    form = CreateWorkoutForm(
        data={
            'title': 'fdsf',
            'description': 'dsfdsf',
            'exercises': [
                {
                    'exercise_id': exercises[0].uuid,
                    'sets': 1,
                    'repetitions': 1,
                    'weight_in_kg': 1,
                },
                {
                    'exercise_id': exercises[1].uuid,
                    'sets': 1,
                    'repetitions': 1,
                    'weight_in_kg': 1,
                },
            ],
        },
        request=None,
    )
    assert form.is_valid() is True


@pytest.mark.django_db
def test_to_be_invalid_with_invalid_exercise_id():
    form = CreateWorkoutForm(
        data={
            'title': 'fdsf',
            'description': 'dsfdsf',
            'exercises': [
                {
                    'exercise_id': 'invalid-uuid',
                    'sets': 1,
                    'repetitions': 1,
                    'weight_in_kg': 1,
                },
            ],
        },
        request=None,
    )
    assert form.is_valid() is False
    assert 'exercises' in form.errors
