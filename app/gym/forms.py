from __future__ import annotations

from typing import Any

from django import forms

from app.core import fields
from app.core.forms import BaseForm, BaseUpdateForm
from app.gym.services.workouts import (
    create_workout,
    get_workout_or_404,
    update_workout,
    validate_workouts_exercises_to_create,
)


class CreateWorkoutExerciseForm(BaseForm):
    exercise_id = forms.UUIDField(required=True)
    sets = forms.IntegerField(required=True)
    repetitions = forms.IntegerField(required=True)


class CreateWorkoutForm(BaseForm):
    name = fields.StrictCharField(required=True)
    description = fields.StrictCharField(required=False)
    exercises = fields.ListField(
        children_field=fields.NestedFormField(
            form_class=CreateWorkoutExerciseForm,
        ),
        required=False,
    )

    def save(self) -> dict:
        exercises, errors = validate_workouts_exercises_to_create(
            self.cleaned_data['exercises']
        )
        if errors:
            raise forms.ValidationError('Some error')

        workout = create_workout(
            user=self.request.user,
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            exercises=exercises,
        )
        return {
            'workout_id': workout.uuid,
            'name': workout.name,
            'description': workout.description,
        }


class UpdateWorkoutExerciseForm(forms.Form):
    workout_exercise_id = forms.UUIDField(required=True)
    exercise_id = forms.UUIDField(required=True)
    repetitions = forms.IntegerField(required=True)
    sets = forms.IntegerField(required=True)
    rest_period = forms.IntegerField(required=True)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        exercise_id = cleaned_data['exercise_id']
        workout_exercise_id = cleaned_data['workout_exercise_id']
        if not exercise_id or not workout_exercise_id:
            raise forms.ValidationError('Invalid exercise or workout exercise id')
        return cleaned_data


class ExercisesInUpdateForm(BaseForm):
    to_create = fields.ListField(
        children_field=fields.NestedFormField(
            form_class=CreateWorkoutExerciseForm,
        ),
    )
    to_update = fields.ListField(
        children_field=fields.NestedFormField(
            form_class=UpdateWorkoutExerciseForm,
        ),
    )


class UpdateWorkoutForm(BaseUpdateForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    workout_has_changed = forms.BooleanField(required=False)
    exercises = fields.NestedFormField(
        form_class=ExercisesInUpdateForm,
        required=False,
    )

    get_or_404_fn = get_workout_or_404

    def save(self, *args, **kwargs):
        update_workout(
            workout=self.instance,
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            exercises=self.cleaned_data['exercises'],
        )


class CreateEquipment(BaseForm):
    ...


class CreateExerciseForm(BaseForm):
    ...
