from app.gym.forms import UpdateWorkoutExerciseForm
from app.gym.repositories.workouts import WorkoutExerciseUpdateDTO
from tests.gym import factories

import pytest


@pytest.mark.django_db
def test_to_return_a_workout_exercise_update_dto():
    workout_exercise = factories.WorkoutExercisesFactory()
    form = UpdateWorkoutExerciseForm(
        data={
            'workout_exercise_id': workout_exercise.uuid,
            'exercise_id': workout_exercise.exercise.uuid,
            'sets': '1',
            'repetitions': '1',
            'weight_in_kg': '1',
        },
    )
    form.is_valid()

    assert isinstance(form.cleaned_data, WorkoutExerciseUpdateDTO)
