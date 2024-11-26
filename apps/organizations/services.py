from django.db import transaction
from django.utils import timezone

from apps.core.utils import clean_model, set_model_fields
from apps.organizations import models


class GymService:
    @transaction.atomic
    def create_gym(
        self,
        user: models.Users,
        gym_data: dict,
    ) -> models.Gym:
        gym = models.Gym(owner=user, **gym_data)
        clean_model(gym)
        gym.save()
        return gym

    @transaction.atomic
    def update_gym(
        self,
        gym: models.Gym,
        gym_data: dict,
    ) -> models.Gym:
        set_model_fields(
            model=gym,
            data=gym_data,
        )
        clean_model(gym)
        gym.save()
        return gym

    @transaction.atomic
    def register_employee(
        self,
        gym: models.Gym,
        user: models.Users,
        role: models.GymEmployee.Roles = models.GymEmployee.Roles.INSTRUCTOR,
    ) -> models.Gym:
        employee = models.GymEmployee(
            user=user,
            gym=gym,
            role=role,
            joined_at=timezone.now(),
        )
        clean_model(employee)
        employee.save()
        return employee

    @transaction.atomic
    def remove_employee(
        self,
        gym: models.Gym,
        employee: models.Users,
    ) -> models.Gym:
        if employee.gym != gym:
            raise ValueError('Employee does not belong to this gym')

        employee.delete()
