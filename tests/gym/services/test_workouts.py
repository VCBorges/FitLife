from app.gym import models
from app.gym.models import Workouts
from app.gym.services import workouts as ws  # workouts service
from app.gym.transfer.workouts import WorkoutExerciseUpdateDTO
from app.users.models import Users
from tests.gym import factories

import pytest


@pytest.mark.django_db
def test_create_workout_to_create_a_workout_without_exercises(mock_user: Users):
    workout = ws.create_workout(
        user=mock_user,
        title='Test Workout',
        description='Test Workout Description',
    )
    workout.refresh_from_db()
    assert isinstance(workout, Workouts)
    assert workout.title == 'Test Workout'
    assert workout.description == 'Test Workout Description'
    assert workout.user == mock_user


@pytest.mark.django_db
def test_create_workout_with_exercises_to_create_workout_exercises(mock_user: Users):
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
    workout_exercises = workout.exercises.all()
    assert workout_exercises.count() == 1
    assert workout_exercises[0].exercise == ex1
    assert workout_exercises[0].repetitions == 10
    assert workout_exercises[0].sets == 3


@pytest.mark.django_db
def test_update_workout_to_update_workout(mock_workout: Workouts):
    ws.update_workout(
        workout=mock_workout,
        name='Updated Workout Name',
        description='Updated Workout Description',
    )
    mock_workout.refresh_from_db()
    assert mock_workout.title == 'Updated Workout Name'
    assert mock_workout.description == 'Updated Workout Description'


@pytest.mark.django_db
def test_update_workout_to_create_a_new_workout_exercise(mock_workout: Workouts):
    ex1 = factories.ExercisesFactory()
    ws.update_workout(
        workout=mock_workout,
        name='Updated Workout Name',
        description='Updated Workout Description',
        exercises=ws.UpdateWorkoutExercisesDict(
            create=[
                ws.WorkoutExerciseCreateDTO(
                    exercise=ex1,
                    repetitions=10,
                    sets=3,
                ),
            ],
        ),
    )
    workout_exercises = mock_workout.exercises.all()
    assert workout_exercises.count() == 1
    assert workout_exercises[0].exercise == ex1
    assert workout_exercises[0].repetitions == 10
    assert workout_exercises[0].sets == 3


@pytest.mark.django_db
def test_update_workout_to_update_existing_workout_exercise(
    mock_workout_with_exercise: Workouts,
):
    ex1 = factories.ExercisesFactory()
    ws.update_workout(
        workout=mock_workout_with_exercise,
        name='Updated Workout Name',
        description='Updated Workout Description',
        exercises=ws.UpdateWorkoutExercisesDict(
            update=[
                WorkoutExerciseUpdateDTO(
                    instance=mock_workout_with_exercise.exercises.first(),
                    exercise=ex1,
                    repetitions=15,
                    sets=5,
                ),
            ],
        ),
    )
    workout_exercises = mock_workout_with_exercise.exercises.all()
    assert workout_exercises.count() == 1
    assert workout_exercises[0].repetitions == 15
    assert workout_exercises[0].sets == 5


@pytest.mark.django_db
def test_update_workout_to_delete_existing_workout_exercise(
    mock_workout_with_exercise: Workouts,
):
    ws.update_workout(
        workout=mock_workout_with_exercise,
        name='Updated Workout Name',
        description='Updated Workout Description',
        exercises=ws.UpdateWorkoutExercisesDict(
            delete=[
                mock_workout_with_exercise.exercises.first(),
            ],
        ),
    )
    workout_exercises = mock_workout_with_exercise.exercises.all()
    assert workout_exercises.count() == 0


@pytest.mark.django_db
def test_update_workout_to_create_update_and_delete_workout_exercises(
    mock_workout_with_exercise: Workouts,
):
    ex1 = factories.ExercisesFactory()
    ex2 = factories.ExercisesFactory()
    ws.update_workout(
        workout=mock_workout_with_exercise,
        name='Updated Workout Name',
        description='Updated Workout Description',
        exercises=ws.UpdateWorkoutExercisesDict(
            create=[
                ws.WorkoutExerciseCreateDTO(
                    exercise=ex1,
                    repetitions=10,
                    sets=3,
                ),
            ],
            update=[
                WorkoutExerciseUpdateDTO(
                    instance=mock_workout_with_exercise.exercises.first(),
                    exercise=ex2,
                    repetitions=15,
                    sets=5,
                ),
            ],
            delete=[
                mock_workout_with_exercise.exercises.last(),
            ],
        ),
    )
    workout_exercises = mock_workout_with_exercise.exercises.all()
    assert workout_exercises.count() == 1
    assert workout_exercises[0].exercise == ex1
    assert workout_exercises[0].repetitions == 10
    assert workout_exercises[0].sets == 3


@pytest.mark.django_db
def test_delete_workout_to_delete_workout(mock_workout: Workouts):
    ws.delete_workout(workout=mock_workout)
    assert Workouts.objects.filter(pk=mock_workout.pk).exists() is False


@pytest.mark.django_db
def test_delete_workout_to_delete_workout_exercises(
    mock_workout_with_exercise: Workouts,
):
    exercises = mock_workout_with_exercise.exercises.all()
    exercices_pks = [ex.pk for ex in exercises]

    ws.delete_workout(workout=mock_workout_with_exercise)

    assert Workouts.objects.filter(pk=mock_workout_with_exercise.pk).exists() is False
    assert (
        models.WorkoutExercises.objects.filter(pk__in=exercices_pks).exists() is False
    )


@pytest.mark.django_db
def test_mark_workout_as_done_to_create_workout_history(mock_workout: Workouts):
    ws.complete_workout(
        workout=mock_workout,
        # user=mock_workout.user,
    )

    workout_history = models.WorkoutHistory.objects.get(workout=mock_workout)

    assert workout_history.workout == mock_workout
    assert workout_history.user == mock_workout.user


@pytest.mark.django_db
def test_complete_workout_to_create_a_workout_history_with_exercises(
    mock_workout_with_exercise: Workouts,
):
    ws.complete_workout(
        workout=mock_workout_with_exercise,
    )

    workout_history = models.WorkoutHistory.objects.get(
        workout=mock_workout_with_exercise
    )
    workout_history_exercises = workout_history.exercises.all()

    assert workout_history_exercises.count() == 1
    assert (
        workout_history_exercises[0].exercise
        == mock_workout_with_exercise.exercises.first().exercise
    )
    assert (
        workout_history_exercises[0].repetitions
        == mock_workout_with_exercise.exercises.first().repetitions
    )
    assert (
        workout_history_exercises[0].sets
        == mock_workout_with_exercise.exercises.first().sets
    )


@pytest.mark.django_db
def test_uncomplete_workout_to_delete_workout_history():
    workout_hist = factories.WorkoutHistoriesFactory()
    workout_hist_pk = workout_hist.pk
    ws.uncomplete_workout(workout_history=workout_hist)

    assert models.WorkoutHistory.objects.filter(pk=workout_hist_pk).exists() is False


@pytest.mark.django_db
def test_uncomplete_workout_to_delete_workout_history_and_its_exercises():
    workout_hist = factories.WorkoutHistoriesFactory(with_exercises=True)
    workout_hist_exercise = factories.WorkoutHistoryExercisesFactory(
        workout_history=workout_hist
    )
    workout_hist_pk = workout_hist.pk
    workout_hist_exercise_pk = workout_hist_exercise.pk

    ws.uncomplete_workout(workout_history=workout_hist)

    assert models.WorkoutHistory.objects.filter(pk=workout_hist_pk).exists() is False
    assert (
        models.WorkoutHistoryExercises.objects.filter(
            pk=workout_hist_exercise_pk
        ).exists()
        is False
    )
