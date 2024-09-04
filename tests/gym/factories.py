from apps.gym import models
from tests.users.factories import UsersFactory

import factory

translatable_field = factory.Dict(
    {
        'en': factory.Faker('word'),
        'es': factory.Faker('word', locale='pt_BR'),
    }
)


class MuscleGroupsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MuscleGroups

    name = translatable_field
    description = translatable_field


class EquipmentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Equipments

    name = translatable_field
    description = translatable_field


class ExercisesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Exercises

    name = translatable_field
    description = translatable_field
    primary_muscle = factory.SubFactory(MuscleGroupsFactory)
    secondary_muscle = factory.SubFactory(MuscleGroupsFactory)
    equipment = factory.SubFactory(EquipmentsFactory)


# FIXME: To have the same user from the workout
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
    user = factory.SubFactory(UsersFactory)
    creator = factory.SubFactory(UsersFactory)

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
    creator = factory.SubFactory(UsersFactory)
    completed_at = factory.Faker('date_time')
    title = factory.Faker('word')
    description = factory.Faker('text')

    class Params:
        with_exercises = factory.Trait(
            exercises=factory.RelatedFactory(
                WorkoutHistoryExercisesFactory, 'workout_history'
            )
        )
        without_exercises = factory.Trait(exercises=None)
