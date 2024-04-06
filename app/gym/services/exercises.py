from django import forms
from django.db.models.query import QuerySet
from django.db.models import F


from app.gym import models
from app.gym.repositories.exercises import ExercisesRepository


def get_exercise_or_404(uuid: str) -> models.Workouts:
    try:
        return ExercisesRepository.get_by_uuid(uuid)
    except models.Workouts.DoesNotExist:
        raise forms.ValidationError('Workout not found')


def get_exercises_select_field_options() -> list[models.Exercises]:
    return (
        list(
            ExercisesRepository
            .list_all()
            .values(
                value=F('uuid'),
                label=F('name'),
            )
        )
    )