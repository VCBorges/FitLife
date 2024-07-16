from app.gym import models as gym_models
from tests.gym import factories as gym_factories
from tests.users.factories import UsersFactory

import pytest


@pytest.mark.django_db
def test_user_factory_to_create_a_user():
    user = UsersFactory()

    assert user.email


@pytest.mark.django_db
def test_workouts_factory_with_exercises():
    workout: gym_models.Workouts = gym_factories.WorkoutsFactory.create(
        with_exercises=True
    )

    assert workout.exercises.count() == 1
    assert workout.exercises.first().exercise
    assert workout.exercises.first().repetitions
    assert workout.exercises.first().sets


@pytest.mark.django_db
def test_workouts_factory_without_exercises():
    workout: gym_models.Workouts = gym_factories.WorkoutsFactory.create(
        without_exercises=True
    )

    assert not workout.exercises.all()


@pytest.mark.django_db
def test_workout_histories_factory_with_exercises():
    workout_history: gym_models.WorkoutHistory = (
        gym_factories.WorkoutHistoriesFactory.create(with_exercises=True)
    )

    assert workout_history.exercises.count() == 1
    assert workout_history.exercises.first().exercise
    assert workout_history.exercises.first().repetitions
    assert workout_history.exercises.first().sets
