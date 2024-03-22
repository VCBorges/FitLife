from gym import models

from core.repositories import BaseRepository


class MuscleGroupReposiory(BaseRepository):
    @staticmethod
    def get_by_id(id: int) -> models.MuscleGroups:
        return models.MuscleGroups.objects.get(pk=id)

    @staticmethod
    def get_by_uuid(uuid: str) -> models.MuscleGroups:
        return models.MuscleGroups.objects.get(uuid=uuid)

    @staticmethod
    def create(
        *,
        name: str,
        description: str | None = None,
    ) -> models.MuscleGroups:
        return models.MuscleGroups(
            name=name,
            description=description,
        )

    @staticmethod
    def update(instance: models.MuscleGroups, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(instance, key, value)

    @staticmethod
    def delete(instance: models.MuscleGroups) -> None:
        instance.delete()
