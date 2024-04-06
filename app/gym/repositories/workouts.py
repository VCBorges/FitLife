from dataclasses import dataclass

from django.db.models import QuerySet

from app.core.repositories import BaseDTO, BaseRepository
from app.gym import models
from app.users.models import Users


@dataclass
class WorkoutUpdateDTO(BaseDTO):
    name: str | None = None
    description: str | None = None


@dataclass
class WorkoutExerciseUpdateDTO(BaseDTO):
    repetitions: int | None = None
    sets: int | None = None
    rest_period: int | None = None


@dataclass
class WorkoutExerciseCreateDTO(BaseDTO):
    exercise: models.Exercises
    repetitions: int = 0
    sets: int = 0
    rest_period: int = 0


class WorkoutsRepository(BaseRepository):
    @staticmethod
    def get_by_id(id: int) -> models.Workouts:
        return models.Workouts.objects.get(pk=id)

    @staticmethod
    def get_by_uuid(uuid: str) -> models.Workouts:
        return models.Workouts.objects.get(uuid=uuid)

    @staticmethod
    def get_all_by_user(user: Users) -> QuerySet[models.Workouts]:
        return models.Workouts.objects.prefetch_related('workout_exercises').filter(
            user=user
        )

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
    def update(
        instance: models.Workouts,
        *,
        dto: WorkoutUpdateDTO,
    ) -> None:
        instance(**dto.to_dict())

    @staticmethod
    def delete(instance: models.Workouts) -> None:
        instance.delete()

    @staticmethod
    def get_exercises(workout: models.Workouts) -> QuerySet[models.WorkoutExercises]:
        return models.WorkoutExercises.objects.filter(workout=workout)

    @staticmethod
    def get_exercise_by_uuid(
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
        dto: WorkoutExerciseCreateDTO,
    ) -> models.WorkoutExercises:
        return models.WorkoutExercises(workout=workout, **dto.to_dict())

    @classmethod
    def bulk_create_exercises(
        cls,
        *,
        workout: models.Workouts,
        exercises: list[WorkoutExerciseCreateDTO],
    ) -> list[models.WorkoutExercises]:
        workout_exercises = [
            cls.create_exercise(
                workout=workout,
                dto=exercise,
            )
            for exercise in exercises
        ]
        models.WorkoutExercises.objects.bulk_create(workout_exercises)
        return workout_exercises

    @staticmethod
    def remove_exercise(instance: models.WorkoutExercises) -> None:
        instance.delete()

    @classmethod
    def update_exercise(
        cls,
        instance: models.WorkoutExercises,
        *,
        dto: WorkoutExerciseUpdateDTO,
    ) -> None:
        instance(**dto.to_dict())

    @classmethod
    def _update_exercise(
        cls,
        instance: models.WorkoutExercises,
        dto: WorkoutExerciseUpdateDTO,
    ) -> models.WorkoutExercises:
        cls.update_exercise(instance, dto=dto)
        return instance

    @classmethod
    def bulk_update_exercises(
        cls,
        excercises: list[tuple[models.WorkoutExercises, WorkoutExerciseUpdateDTO]],
    ) -> None:
        exercises_to_update = [
            cls._update_exercise(instance=exercise, dto=dto)
            for exercise, dto in excercises
        ]
        models.WorkoutExercises.objects.bulk_update(
            exercises_to_update, fields=WorkoutExerciseUpdateDTO.get_field_names()
        )
