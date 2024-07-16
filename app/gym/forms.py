from __future__ import annotations

from django import forms

from app.core import fields
from app.core.forms import BaseForm, BaseInstanceForm
from app.gym import models
from app.gym.repositories.workouts import (
    WorkoutExerciseCreateDTO,
    WorkoutExerciseUpdateDTO,
)
from app.gym.services.workouts import (
    create_workout,
    delete_workout,
    update_workout,
)


class CreateWorkoutExerciseForm(BaseForm):
    exercise_id = fields.ModelField(
        required=True,
        model_class=models.Exercises,
    )
    sets = forms.IntegerField(required=True)
    repetitions = forms.IntegerField(required=True)
    weight_in_kg = forms.IntegerField(required=True)
    rest_period = forms.IntegerField(required=False)

    def clean(self) -> WorkoutExerciseCreateDTO:
        cleaned_data = super().clean()
        return WorkoutExerciseCreateDTO(
            exercise=cleaned_data.get('exercise_id', None),
            sets=cleaned_data.get('sets', None),
            repetitions=cleaned_data.get('repetitions', None),
            weight_in_kg=cleaned_data.get('weight_in_kg', None),
            rest_period=cleaned_data.get('rest_period', None),
        )


class CreateWorkoutForm(BaseForm):
    title = fields.StrictCharField(required=True)
    description = fields.StrictCharField(required=False)
    exercises = fields.ListField(
        children_field=fields.NestedFormField(
            form_class=CreateWorkoutExerciseForm,
        ),
        required=False,
    )

    def save(self) -> dict:
        workout = create_workout(
            user=self.request.user,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            exercises=self.cleaned_data['exercises'],
        )
        return {
            'workout_id': workout.uuid,
            'title': workout.title,
            'description': workout.description,
        }


class UpdateWorkoutExerciseForm(forms.Form):
    workout_exercise_id = fields.ModelField(
        required=True,
        model_class=models.WorkoutExercises,
    )
    exercise_id = fields.ModelField(required=True, model_class=models.Exercises)
    repetitions = forms.IntegerField(required=True)
    sets = forms.IntegerField(required=True)
    rest_period = forms.IntegerField(required=True)

    def clean(self) -> tuple[models.WorkoutExercises, WorkoutExerciseUpdateDTO]:
        cleaned_data = super().clean()
        return WorkoutExerciseUpdateDTO(
            instance=cleaned_data.get('workout_exercise_id', None),
            exercise=cleaned_data.get('exercise_id', None),
            sets=cleaned_data.get('sets', None),
            repetitions=cleaned_data.get('repetitions', None),
        )


class ModifiedExercisesForm(BaseForm):
    create = fields.ListField(
        children_field=fields.NestedFormField(
            form_class=CreateWorkoutExerciseForm,
        ),
    )
    update = fields.ListField(
        children_field=fields.NestedFormField(
            form_class=UpdateWorkoutExerciseForm,
        ),
    )
    delete = fields.ListField(
        children_field=fields.ModelField(
            model_class=models.WorkoutExercises,
        ),
    )


class UpdateWorkoutForm(BaseInstanceForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    exercises = fields.NestedFormField(
        form_class=ModifiedExercisesForm,
        required=False,
    )

    model_class = models.Workouts

    def save(self, *args, **kwargs):
        update_workout(
            workout=self.instance,
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            exercises=self.cleaned_data['exercises'],
        )


class DeleteWorkoutForm(BaseInstanceForm[models.Workouts]):
    model_class = models.Workouts

    def save(self):
        delete_workout(self.instance)


class CompleteWorkoutForm(BaseInstanceForm[models.Workouts]):
    model_class = models.Workouts

    def save(self):
        ...
        # workout_history = complete_workout(self.instance)
