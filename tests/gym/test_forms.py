from src.gym import forms
from tests.gym import factories

import pytest
from rich import print  # noqa


@pytest.mark.django_db
def test_CreateWorkoutExerciseForm_to_return_cleaned_data():
    exercise = factories.ExercisesFactory()
    print(f'{exercise = }')

    data = {
        'exercise_id': exercise.id,
        'sets': 3,
        'reps': 10,
        'weight': 50.0,
        'rest_period': 60,
    }

    form = forms.CreateWorkoutExerciseForm(data=data)

    form.is_valid()

    print(f'{form.cleaned_data = }')
    print(f'{form.errors = }')
