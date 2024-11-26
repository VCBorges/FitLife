from apps.gym import models
from tests.users.factories import UsersFactory

import factory

translatable_field = factory.Dict(
    {
        'en': factory.Faker('word'),
        'pt': factory.Faker('word', locale='pt_BR'),
    }
)


class MuscleGroupsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MuscleGroup

    name = translatable_field
    description = translatable_field


class EquipmentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Equipment

    name = translatable_field
    description = translatable_field


class ExercisesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Exercise

    name = translatable_field
    description = translatable_field
    primary_muscle = factory.SubFactory(MuscleGroupsFactory)
    secondary_muscle = factory.SubFactory(MuscleGroupsFactory)
    equipment = factory.SubFactory(EquipmentsFactory)


# FIXME: To have the same user from the workout
class WorkoutExercisesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkoutExercise

    workout = factory.SubFactory('tests.gym.factories.WorkoutsFactory')
    exercise = factory.SubFactory(ExercisesFactory)
    repetitions = factory.Faker('random_int', min=1, max=10)
    sets = factory.Faker('random_int', min=1, max=10)


class WorkoutsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Workout

    user = factory.SubFactory(UsersFactory)
    title = factory.Faker('word')
    description = factory.Faker('text')
    creator = factory.SelfAttribute('user')

    class Params:
        with_exercises = factory.Trait(
            exercises=factory.RelatedFactory(
                factory=WorkoutExercisesFactory,
                factory_related_name='workout',
            )
        )


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
