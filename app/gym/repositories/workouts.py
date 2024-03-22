from django.db.models import QuerySet

from app.core.repositories import BaseRepository
from app.gym import models
from app.users.models import Users


class WorkoutsRepository(BaseRepository):
    @staticmethod
    def get_by_id(id: int) -> models.Workouts:
        return models.Workouts.objects.get(pk=id)

    @staticmethod
    def get_by_uuid(uuid: str) -> models.Workouts:
        return models.Workouts.objects.get(uuid=uuid)

    @staticmethod
    def create(
        *,
        name: str,
        user: Users,
        description: str | None = None,
    ) -> models.Workouts:
        return models.Workouts(
            name=name,
            description=description,
            user=user,
        )

    @staticmethod
    def update(instance: models.Workouts, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(instance, key, value)

    @staticmethod
    def delete(instance: models.Workouts) -> None:
        instance.delete()

    @staticmethod
    def get_exercises(workout: models.Workouts) -> QuerySet[models.WorkoutExercises]:
        return models.WorkoutExercises.objects.filter(workout=workout)

    @staticmethod
    def _get_exercise_by_uuid(
        *,
        workout: models.Workouts,
        exercise_uuid: str,
    ) -> models.WorkoutExercises:
        return models.WorkoutExercises.objects.get(
            workout=workout,
            uuid=exercise_uuid,
        )

    @staticmethod
    def create_exercise(
        *,
        workout: models.Workouts,
        exercise: models.Exercises,
        repetitions: int,
        sets: int,
        rest_period: int,
    ) -> models.WorkoutExercises:
        return models.WorkoutExercises(
            workout=workout,
            exercise=exercise,
            repetitions=repetitions,
            sets=sets,
            rest_period=rest_period,
        )

    @classmethod
    def remove_exercise_by_uuid(
        cls,
        *,
        workout: models.Workouts,
        exercise_uuid: str,
    ) -> None:
        workout_exercise = cls._get_exercise_by_uuid(
            workout=workout,
            exercise_uuid=exercise_uuid,
        )
        workout_exercise.delete()

    @classmethod
    def update_exercise_by_uuid(
        cls,
        *,
        workout: models.Workouts,
        exercise_uuid: str,
        repetitions: int,
        sets: int,
        rest_period: int,
    ) -> models.WorkoutExercises:
        workout_exercise = cls._get_exercise_by_uuid(
            workout=workout,
            exercise_uuid=exercise_uuid,
        )
        workout_exercise.repetitions = repetitions
        workout_exercise.sets = sets
        workout_exercise.rest_period = rest_period
        workout_exercise.save()
        return workout_exercise
