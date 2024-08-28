from apps.gym import models
from apps.gym.services import WorkoutService
from apps.gym.typed import CreateWorkoutExerciseSchema
from tests.gym import factories

import pytest


@pytest.fixture
def exercises_to_create() -> list[CreateWorkoutExerciseSchema]:
    return [
        {
            'exercise': factories.ExercisesFactory(),
            'sets': 3,
            'repetitions': 10,
            'rest_period': 60,
            'weight': 20.0,
        },
        {
            'exercise': factories.ExercisesFactory(),
            'sets': 4,
            'repetitions': 8,
            'rest_period': 90,
            'weight': 30.0,
        },
        {
            'exercise': factories.ExercisesFactory(),
            'sets': 5,
            'repetitions': 6,
            'rest_period': 120,
            'weight': 40.0,
        },
    ]


@pytest.mark.django_db
def test_create_workout_to_create_a_workout_without_exercises():
    user = factories.UsersFactory()
    workout_service = WorkoutService()
    workout = workout_service.create_workout(
        user=user,
        title='Workout 1',
    )
    assert workout.title == 'Workout 1'
    assert workout.description is None
    assert workout.user == user
    assert workout.workout_exercises.count() == 0


@pytest.mark.django_db
def test_create_workout_to_create_workout_exercises(
    exercises_to_create: list[CreateWorkoutExerciseSchema],
):
    user = factories.UsersFactory()
    workout_service = WorkoutService()
    workout = workout_service.create_workout(
        user=user,
        title='Workout 1',
        exercises=exercises_to_create,
    )
    assert workout.workout_exercises.count() == 3


@pytest.mark.django_db
def test_create_workout_to_exercises_have_the_correct_attrs(
    exercises_to_create: list[CreateWorkoutExerciseSchema],
):
    user = factories.UsersFactory()
    workout_service = WorkoutService()
    workout = workout_service.create_workout(
        user=user,
        title='Workout 1',
        exercises=exercises_to_create,
    )
    for i, exercise in enumerate(workout.workout_exercises.all()):
        assert exercise.exercise == exercises_to_create[i]['exercise']
        assert exercise.sets == exercises_to_create[i]['sets']
        assert exercise.repetitions == exercises_to_create[i]['repetitions']
        assert exercise.rest_period == exercises_to_create[i]['rest_period']
        assert exercise.weight == exercises_to_create[i]['weight']


@pytest.mark.django_db
def test_update_workout_to_update_workout_attrs():
    workout = factories.WorkoutsFactory()
    workout_service = WorkoutService()
    workout = workout_service.update_workout(
        workout=workout,
        title='Workout 2',
        description='Workout 2 description',
    )
    assert workout.title == 'Workout 2'
    assert workout.description == 'Workout 2 description'


@pytest.mark.django_db
def test_update_workout_to_delete_exercises():
    user = factories.UsersFactory()
    workout = factories.WorkoutsFactory(
        with_exercises=True,
        user=user,
    )
    execises_count_before = workout.workout_exercises.count()
    workout_service = WorkoutService()
    workout = workout_service.update_workout(
        workout=workout,
        title='Workout 2',
        exercises={'delete': workout.workout_exercises.all()},
    )
    execises_count_after = workout.workout_exercises.count()

    assert execises_count_before > 0
    assert execises_count_after == 0


@pytest.mark.django_db
def test_update_workout_to_create_exercises(
    exercises_to_create: list[CreateWorkoutExerciseSchema],
):
    workout = factories.WorkoutsFactory()
    workout_service = WorkoutService()
    workout = workout_service.update_workout(
        workout=workout,
        title='Workout 2',
        exercises={'create': exercises_to_create},
    )
    assert workout.workout_exercises.count() == 3


@pytest.mark.django_db
def test_complete_workout_to_create_workout_history():
    workout = factories.WorkoutsFactory()

    workkout_history = WorkoutService().complete_workout(
        user=workout.user,
        workout=workout,
    )
    assert isinstance(workkout_history, models.WorkoutHistory)


@pytest.mark.django_db
def test_complete_workout_to_create_a_workout_with_the_same_attrs():
    workout = factories.WorkoutsFactory()

    workkout_history = WorkoutService().complete_workout(
        user=workout.user,
        workout=workout,
    )

    assert workkout_history.title == workout.title
    assert workkout_history.description == workout.description
    assert workkout_history.user == workout.user
    assert workkout_history.workout == workout


@pytest.mark.django_db
def test_complete_workout_to_create_workout_history_exercises():
    workout: models.Workouts = factories.WorkoutsFactory(with_exercises=True)

    workout_history = WorkoutService().complete_workout(
        user=workout.user,
        workout=workout,
    )

    assert workout_history.exercises.count() == workout.workout_exercises.count()
    for i, exercise in enumerate(workout.workout_exercises.all()):
        assert workout_history.exercises.all()[i].exercise == exercise.exercise
        assert workout_history.exercises.all()[i].sets == exercise.sets
        assert workout_history.exercises.all()[i].repetitions == exercise.repetitions
        assert workout_history.exercises.all()[i].rest_period == exercise.rest_period
        assert workout_history.exercises.all()[i].weight == exercise.weight


@pytest.mark.django_db
def test_uncomplete_workout_to_delete_a_workout_history():
    workout_history = factories.WorkoutHistoriesFactory()

    WorkoutService().uncomplete_workout(workout_history)

    assert models.WorkoutHistory.objects.filter(id=workout_history.id).count() == 0


@pytest.mark.django_db
def test_uncomplete_workout_to_delete_workout_history_exercises():
    workout_history = factories.WorkoutHistoriesFactory(with_exercises=True)

    WorkoutService().uncomplete_workout(workout_history)

    assert models.WorkoutHistoryExercises.objects.count() == 0


@pytest.mark.django_db
def test_clone_workout_to_create_a_new_workout_with_the_same_attrs():
    workout = factories.WorkoutsFactory()
    user = factories.UsersFactory()

    workout_clone = WorkoutService().clone_workout(
        user=user,
        workout=workout,
    )

    assert workout_clone.title == workout.title
    assert workout_clone.description == workout.description
    assert workout_clone.user != workout.user
    assert workout_clone.creator == workout.creator
    assert workout_clone.workout_exercises.count() == workout.workout_exercises.count()
