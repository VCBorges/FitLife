from apps.gym import forms
from tests.gym import factories

import pytest
from rich import print  # noqa


@pytest.mark.django_db
def test_CreateWorkoutExerciseForm_cleaned_data_with_valid_input_to_have_expected_keys():
    # Arrange
    expected_keys = [
        'exercise',
        'sets',
        'repetitions',
        'weight',
        'rest_period',
        'notes',
    ]

    exercise = factories.ExercisesFactory()
    workout_exercise = factories.WorkoutExercisesFactory()
    data = {
        'workout_exercise_id': workout_exercise.pk,
        'exercise_id': exercise.pk,
        'sets': 3,
        'repetitions': 10,
        'weight': 50.0,
        'rest_period': 60,
    }
    form = forms.CreateWorkoutExerciseForm(data=data)

    # Act
    form.is_valid(raise_exception=False)

    # Assert
    assert set(form.cleaned_data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_CreateWorkoutForm_cleaned_data_with_valid_input_to_have_expected_keys():
    # Arrange
    expected_keys = [
        'title',
        'description',
        'exercises',
    ]

    data = {
        'title': 'Test workout',
        'description': 'Test workout description',
        'exercises': [
            {
                'workout_exercise_id': factories.WorkoutExercisesFactory().pk,
                'exercise_id': factories.ExercisesFactory().pk,
                'sets': 3,
                'repetitions': 10,
                'weight': 50.0,
                'rest_period': 60,
            },
        ],
    }
    form = forms.CreateWorkoutForm(data=data)

    # Act
    form.is_valid(raise_exception=False)

    # Assert
    assert set(form.cleaned_data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_UpdateWorkoutExerciseForm_cleaned_data_with_valid_input_to_have_expected_keys():
    # Arrange
    expected_keys = [
        'workout_exercise',
        'sets',
        'repetitions',
        'weight',
        'rest_period',
    ]

    exercise = factories.ExercisesFactory()
    workout_exercise = factories.WorkoutExercisesFactory()
    data = {
        'workout_exercise_id': workout_exercise.pk,
        'exercise_id': exercise.pk,
        'sets': 3,
        'repetitions': 10,
        'weight': 50.0,
        'rest_period': 60,
    }
    form = forms.UpdateWorkoutExerciseForm(data=data)

    # Act
    form.is_valid(raise_exception=False)

    # Assert
    assert set(form.cleaned_data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_DeleteWorkoutExerciseForm_cleaned_data_with_valid_input_to_have_expected_keys():
    # Arrange
    expected_keys = [
        'workout_exercise',
    ]

    workout_exercise = factories.WorkoutExercisesFactory()
    data = {
        'workout_exercise_id': workout_exercise.pk,
    }
    form = forms.DeleteWorkoutExerciseForm(data=data)

    # Act
    form.is_valid(raise_exception=False)

    # Assert
    assert set(form.cleaned_data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_WorkoutExercisesUpdateWorkoutForm_cleaned_data_with_valid_to_have_expected_keys():
    # Arrange
    expected_keys = [
        'to_create',
        'to_update',
        'to_delete',
    ]

    workout_exercise = factories.WorkoutExercisesFactory()
    exercise = factories.ExercisesFactory()
    data = {
        'to_create': [
            {
                'workout_exercise_id': workout_exercise.pk,
                'exercise_id': exercise.pk,
                'sets': 3,
                'repetitions': 10,
                'weight': 50.0,
                'rest_period': 60,
            }
        ],
        'to_update': [
            {
                'workout_exercise_id': workout_exercise.pk,
                'exercise_id': exercise.pk,
                'sets': 3,
                'repetitions': 10,
                'weight': 50.0,
                'rest_period': 60,
            }
        ],
        'to_delete': [
            {
                'workout_exercise_id': workout_exercise.pk,
            }
        ],
    }
    form = forms.WorkoutExercisesUpdateWorkoutForm(data=data)

    # Act
    form.is_valid(raise_exception=False)
    print(f'{form.errors = }')

    # Assert
    assert set(form.cleaned_data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_UpdateWorkoutForm_cleaned_data_with_valid_input_to_have_expected_keys():
    # Arrange
    expected_keys = [
        'title',
        'description',
        'exercises',
    ]
    workout_exercise = factories.WorkoutExercisesFactory()
    exercise = factories.ExercisesFactory()
    data = {
        'title': 'Test workout',
        'description': 'Test workout description',
        'exercises': {
            'to_create': [
                {
                    'exercise_id': exercise.pk,
                    'sets': 3,
                    'repetitions': 10,
                    'weight': 50.0,
                    'rest_period': 60,
                },
            ],
            'to_update': [
                {
                    'workout_exercise_id': workout_exercise.pk,
                    'sets': 3,
                    'repetitions': 10,
                    'weight': 50.0,
                    'rest_period': 60,
                },
            ],
            'to_delete': [
                {'workout_exercise_id': workout_exercise.pk},
            ],
        },
    }
    form = forms.UpdateWorkoutForm(data=data)

    # Act
    form.is_valid(raise_exception=False)

    # Assert
    assert set(form.cleaned_data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_CompleteWorkoutExerciseForm_to_have_expected_keys():
    expected_keys = [
        'workout_exercise',
        'sets',
        'repetitions',
        'weight',
        'rest_period',
    ]
    workout_exercise = factories.WorkoutExercisesFactory()
    data = {
        'workout_exercise_id': workout_exercise.pk,
        'sets': 3,
        'repetitions': 10,
        'weight': 50.0,
        'rest_period': 60,
    }
    form = forms.CompleteWorkoutExerciseForm(data=data)

    form.is_valid(raise_exception=False)

    assert set(form.cleaned_data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_CompleteWorkoutForm_to_have_expected_keys():
    expected_keys = [
        'exercises',
    ]
    workout_exercise = factories.WorkoutExercisesFactory()
    data = {
        'exercises': [
            {
                'workout_exercise_id': workout_exercise.pk,
                'sets': 3,
                'repetitions': 10,
                'weight': 50.0,
                'rest_period': 60,
            }
        ],
    }
    form = forms.CompleteWorkoutForm(data=data)

    form.is_valid(raise_exception=False)

    assert set(form.cleaned_data.keys()) == set(expected_keys)
