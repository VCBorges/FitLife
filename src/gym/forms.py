from django import forms

from src.core import form_fields
from src.core.forms import BaseForm
from src.gym import models


class CreateWorkoutExerciseForm(BaseForm):
    exercise_id = forms.ModelChoiceField(queryset=models.Exercises.objects.all())
    sets = forms.IntegerField(required=False)
    repetitions = forms.IntegerField(required=False)
    weight = forms.FloatField(required=False)
    rest_period = forms.IntegerField(required=False)

    normalized_fields_mapping = {
        'exercise_id': 'exercise',
    }


class CreateWorkoutForm(BaseForm):
    title = forms.CharField(max_length=255)
    description = forms.CharField(required=False)
    exercises = form_fields.NestedFormField(
        form_class=CreateWorkoutExerciseForm,
        required=False,
    )
