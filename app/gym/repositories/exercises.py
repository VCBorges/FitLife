from gym import models

from core.repositories import BaseRepository


class ExercisesRepository(BaseRepository):
    @staticmethod
    def get_by_id(id: int) -> models.Exercises:
        return models.Exercises.objects.get(pk=id)

    @staticmethod
    def get_by_uuid(uuid: str) -> models.Exercises:
        return models.Exercises.objects.get(uuid=uuid)

    @staticmethod
    def create(
        *,
        name: str,
        description: str | None = None,
        equipment: models.Equipments | None = None,
    ) -> models.Exercises:
        return models.Exercises(
            name=name,
            description=description,
            equipment=equipment,
        )

    @staticmethod
    def update(instance: models.Exercises, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()

    @staticmethod
    def delete(instance: models.Exercises) -> None:
        instance.delete()
