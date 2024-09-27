from apps.gym import models, typed
from apps.gym.services import WorkoutService
from tests.gym import factories

import pytest


def workout_exercises_to_complete(
    workout: models.Workouts,
) -> typed.CompleteWorkoutExerciseSchema:
    return {
        'workout_exercise': factories.WorkoutExercisesFactory(workout=workout),
        'repetitions': 10,
        'sets': 3,
        'weight': 50.0,
        'rest_period': 60,
    }


@pytest.fixture
def workout_exercises_to_create() -> list[typed.CreateWorkoutExerciseSchema]:
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
    workout_exercises_to_create: list[typed.CreateWorkoutExerciseSchema],
):
    user = factories.UsersFactory()
    workout_service = WorkoutService()
    workout = workout_service.create_workout(
        user=user,
        title='Workout 1',
        exercises=workout_exercises_to_create,
    )
    assert workout.workout_exercises.count() == 3


@pytest.mark.django_db
def test_create_workout_to_exercises_have_the_correct_attrs(
    workout_exercises_to_create: list[typed.CreateWorkoutExerciseSchema],
):
    user = factories.UsersFactory()
    workout_service = WorkoutService()
    workout = workout_service.create_workout(
        user=user,
        title='Workout 1',
        exercises=workout_exercises_to_create,
    )
    for i, exercise in enumerate(workout.workout_exercises.all()):
        assert exercise.exercise == workout_exercises_to_create[i]['exercise']
        assert exercise.sets == workout_exercises_to_create[i]['sets']
        assert exercise.repetitions == workout_exercises_to_create[i]['repetitions']
        assert exercise.rest_period == workout_exercises_to_create[i]['rest_period']
        assert exercise.weight == workout_exercises_to_create[i]['weight']


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
        exercises={
            'to_delete': [
                {'workout_exercise': workout.workout_exercises.first()},
            ]
        },
    )
    execises_count_after = workout.workout_exercises.count()

    assert execises_count_before > 0
    assert execises_count_after == 0


@pytest.mark.django_db
def test_update_workout_to_create_exercises(
    workout_exercises_to_create: list[typed.CreateWorkoutExerciseSchema],
):
    print(f'{workout_exercises_to_create = }')
    workout = factories.WorkoutsFactory()
    workout_service = WorkoutService()
    workout = workout_service.update_workout(
        workout=workout,
        title='Workout 2',
        exercises={'to_create': workout_exercises_to_create},
    )
    print(f'{workout.workout_exercises.count() = }')
    assert workout.workout_exercises.count() == 3


@pytest.mark.django_db
def test_complete_workout_to_create_workout_history():
    workout = factories.WorkoutsFactory()

    WorkoutService().complete_workout(
        user=workout.user,
        workout=workout,
        exercises=[
            workout_exercises_to_complete(workout),
        ],
    )
    assert models.WorkoutHistory.objects.filter(workout=workout).count() == 1


@pytest.mark.django_db
def test_complete_workout_to_create_a_workout_history_with_the_same_attrs_as_the_source_workout():
    workout = factories.WorkoutsFactory()

    workout_history = WorkoutService().complete_workout(
        user=workout.user,
        workout=workout,
        exercises=[
            workout_exercises_to_complete(workout),
        ],
    )

    assert workout_history.title == workout.title
    assert workout_history.description == workout.description
    assert workout_history.user == workout.user
    assert workout_history.workout == workout


@pytest.mark.django_db
def test_complete_workout_to_create_a_workout_history_exercise():
    workout: models.Workouts = factories.WorkoutsFactory()

    workout_history = WorkoutService().complete_workout(
        user=workout.user,
        workout=workout,
        exercises=[
            workout_exercises_to_complete(workout),
        ],
    )

    assert workout_history.exercises.count() == 1


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
