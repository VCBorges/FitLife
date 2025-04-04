from dataclasses import dataclass

from django.db import transaction
from django.utils import timezone

from apps.core.utils import clean_model, update_model_fields
from apps.gym.models import Workout
from apps.gym.services import WorkoutService
from apps.organizations import models
from apps.users.services import UserService


class GymService:
    @transaction.atomic
    def create_gym(
        self,
        user: models.Users,
        data: dict,
    ) -> models.Gym:
        gym = models.Gym(owner=user, **data)
        clean_model(gym)
        gym.save()
        return gym

    @transaction.atomic
    def update_gym(
        self,
        gym: models.Gym,
        gym_data: dict,
    ) -> models.Gym:
        update_model_fields(
            model=gym,
            data=gym_data,
        )
        clean_model(gym)
        gym.save()
        return gym

    @transaction.atomic
    def register_employee(
        self,
        *,
        gym: models.Gym,
        data: dict,
    ) -> models.GymEmployee:
        user = UserService.create_user(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            document=data['document'],
            phone=data['phone'],
        )
        employee = models.GymEmployee(
            user=user,
            gym=gym,
            role=data['role'],
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

    # @transaction.atomic
    # def


@dataclass
class ProfessorService:
    professor: models.GymEmployee

    @transaction.atomic
    def create_workout(
        self,
        data: dict,
    ) -> Workout:
        return WorkoutService().create_workout(
            creator=self.professor.user,
            user=data['student'],
            title=data['title'],
            description=data['description'],
            exercises=data['exercises'],
        )
