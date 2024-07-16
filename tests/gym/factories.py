from app.gym import models
from tests.users.factories import UsersFactory

import factory


class MuscleGroupsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MuscleGroups

    name = factory.Faker('word')
    description = factory.Faker('text')


class EquipmentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Equipments

    name = factory.Faker('word')
    description = factory.Faker('text')


class ExercisesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Exercises

    name = factory.Faker('word')
    description = factory.Faker('text')
    primary_muscle = factory.SubFactory(MuscleGroupsFactory)
    secondary_muscle = factory.SubFactory(MuscleGroupsFactory)
    use_equipment = factory.Faker('boolean')


class WorkoutExercisesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkoutExercises

    workout = factory.SubFactory('tests.gym.factories.WorkoutsFactory')
    exercise = factory.SubFactory(ExercisesFactory)
    repetitions = factory.Faker('random_int', min=1, max=10)
    sets = factory.Faker('random_int', min=1, max=10)


class WorkoutsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Workouts

    user = factory.SubFactory(UsersFactory)
    title = factory.Faker('word')
    description = factory.Faker('text')

    class Params:
        with_exercises = factory.Trait(
            exercises=factory.RelatedFactory(WorkoutExercisesFactory, 'workout')
        )
        without_exercises = factory.Trait(exercises=None)


class WorkoutHistoryExercisesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkoutHistoryExercises

    workout_history = factory.SubFactory('tests.gym.factories.WorkoutHistoriesFactory')
    exercise = factory.SubFactory(ExercisesFactory)
    repetitions = factory.Faker('random_int', min=1, max=10)
    sets = factory.Faker('random_int', min=1, max=10)


class WorkoutHistoriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkoutHistory

    user = factory.SubFactory(UsersFactory)
    workout = factory.SubFactory(WorkoutsFactory)
    completed_at = factory.Faker('date_time')

    class Params:
        with_exercises = factory.Trait(
            exercises=factory.RelatedFactory(
                WorkoutHistoryExercisesFactory, 'workout_history'
            )
        )
        without_exercises = factory.Trait(exercises=None)
