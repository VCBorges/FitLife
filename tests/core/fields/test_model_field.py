from django import forms

from app.core.fields import ModelField
from app.gym import models
from tests.gym import factories

import pytest


@pytest.mark.django_db
def test_clean_to_raise_an_exeption_when_the_instance_not_exists():
    field = ModelField(model_class=models.Exercises)
    with pytest.raises(forms.ValidationError):
        field.clean('810beb30-e88b-4d87-9d4f-4c925bf01153')


@pytest.mark.django_db
def test_clean_to_return_the_instance():
    exercise = factories.ExercisesFactory()
    field = ModelField(model_class=models.Exercises)
    assert field.clean(str(exercise.uuid)) == exercise
