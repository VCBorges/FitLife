from app.gym.forms import CreateWorkoutExerciseForm
from tests.gym.factories import ExercisesFactory

import pytest


@pytest.mark.django_db
def test_to_be_valid_with_all_fields_filled():
    exercise = ExercisesFactory()
    form = CreateWorkoutExerciseForm(
        data={
            'exercise_id': exercise.uuid,
            'sets': '1',
            'repetitions': '1',
            'weight_in_kg': '1',
        },
        request=None,
    )
    assert form.is_valid() is True


@pytest.mark.django_db
def test_clean_to_return_workout_exercise_dto():
    exercise = ExercisesFactory()
    form = CreateWorkoutExerciseForm(
        data={
            'exercise_id': exercise.uuid,
            'sets': '1',
            'repetitions': '1',
            'weight_in_kg': '1',
        },
        request=None,
    )
    form.is_valid()

    dto = form.cleaned_data

    assert dto.exercise == exercise
    assert dto.sets == 1
    assert dto.repetitions == 1
    assert dto.weight_in_kg == 1
    assert dto.rest_period is None


@pytest.mark.django_db
def test_to_not_raise_an_exception_when_the_form_in_invalid():
    form = CreateWorkoutExerciseForm(
        data={},
        request=None,
    )

    assert form.is_valid() is False
