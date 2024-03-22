from gym import models

from core.repositories import BaseRepository


class EquipmentsRepository(BaseRepository):
    @staticmethod
    def get_by_id(id: int) -> models.Equipments:
        return models.Equipments.objects.get(pk=id)

    @staticmethod
    def get_by_uuid(uuid: str) -> models.Equipments:
        return models.Equipments.objects.get(uuid=uuid)

    @staticmethod
    def create(
        *,
        name: str,
        description: str | None = None,
    ) -> models.Equipments:
        return models.Equipments(
            name=name,
            description=description,
        )

    @staticmethod
    def update(instance: models.Equipments, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()

    @staticmethod
    def delete(instance: models.Equipments) -> None:
        instance.delete()
