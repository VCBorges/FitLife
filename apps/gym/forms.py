import datetime
from typing import Any

from django import forms

from apps.core import form_fields
from apps.core.forms import BaseForm
from apps.core.utils import get_tomorrow
from apps.gym import models


class CreateWorkoutExerciseForm(BaseForm):
    exercise_id = forms.ModelChoiceField(
        queryset=models.Exercises.objects.all(),
        required=True,
    )
    sets = forms.IntegerField(required=False, min_value=0)
    repetitions = forms.IntegerField(required=False, min_value=0)
    weight = forms.FloatField(required=False, min_value=0)
    rest_period = forms.IntegerField(required=False, min_value=0)
    notes = forms.CharField(required=False)

    normalized_fields_mapping = {
        'exercise_id': 'exercise',
    }


class CreateWorkoutForm(BaseForm):
    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(required=False)
    exercises = form_fields.ListField(
        children_field=form_fields.NestedFormField(
            form_class=CreateWorkoutExerciseForm,
        ),
        required=False,
    )


class UpdateWorkoutExerciseForm(BaseForm):
    workout_exercise_id = forms.ModelChoiceField(
        queryset=models.WorkoutExercises.objects.all(),
        required=True,
    )
    sets = forms.IntegerField(required=False)
    repetitions = forms.IntegerField(required=False)
    weight = forms.FloatField(required=False)
    rest_period = forms.IntegerField(required=False)

    normalized_fields_mapping = {
        'workout_exercise_id': 'workout_exercise',
    }


class DeleteWorkoutExerciseForm(BaseForm):
    workout_exercise_id = forms.ModelChoiceField(
        queryset=models.WorkoutExercises.objects.all()
    )

    normalized_fields_mapping = {
        'workout_exercise_id': 'workout_exercise',
    }


class WorkoutExercisesUpdateWorkoutForm(BaseForm):
    to_create = form_fields.ListField(
        children_field=form_fields.NestedFormField(
            form_class=CreateWorkoutExerciseForm,
        ),
        required=False,
    )
    to_update = form_fields.ListField(
        children_field=form_fields.NestedFormField(
            form_class=UpdateWorkoutExerciseForm,
        ),
        required=False,
    )
    to_delete = form_fields.ListField(
        children_field=form_fields.NestedFormField(
            form_class=DeleteWorkoutExerciseForm,
        ),
        required=False,
    )


class UpdateWorkoutForm(BaseForm):
    title = forms.CharField(max_length=255)
    description = forms.CharField(required=False)
    exercises = form_fields.NestedFormField(
        form_class=WorkoutExercisesUpdateWorkoutForm,
        required=False,
    )


class CompleteWorkoutExerciseForm(BaseForm):
    workout_exercise_id = forms.ModelChoiceField(
        queryset=models.WorkoutExercises.objects.all(),
        required=True,
    )
    is_done = forms.BooleanField(required=False)
    repetitions = forms.IntegerField(required=True, min_value=1)
    sets = forms.IntegerField(required=True, min_value=1)
    weight = forms.IntegerField(required=True, min_value=0)
    rest_period = forms.IntegerField(required=True, min_value=0)

    normalized_fields_mapping = {
        'workout_exercise_id': 'workout_exercise',
    }


class CompleteWorkoutForm(BaseForm):
    exercises = form_fields.ListField(
        children_field=form_fields.NestedFormField(
            form_class=CompleteWorkoutExerciseForm,
        ),
        required=True,
    )

    def clean_exercises(self):
        exercises = self.cleaned_data['exercises']
        if not all(
            exercise['workout_exercise'].workout == self.instance
            for exercise in exercises
        ):
            self.add_error('exercises', 'Invalid workout exercises')
        return exercises


class CreateWorkoutHistoryForm(BaseForm):
    workout_id = forms.ModelChoiceField(
        queryset=models.Workouts.objects.all(),
        required=True,
    )
    exercises = form_fields.ListField(
        children_field=form_fields.NestedFormField(
            form_class=CompleteWorkoutExerciseForm,
        ),
        required=True,
    )

    normalized_fields_mapping = {
        'workout_id': 'workout',
    }

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        exercises = cleaned_data.get('exercises')
        if not all(
            exercise['workout_exercise'].workout == cleaned_data['workout']
            for exercise in exercises
        ):
            # self.add_error('exercises', 'Invalid workout exercises')
            raise forms.ValidationError('Invalid workout exercises')
        return cleaned_data


class FilterWorkoutHistoriesForm(BaseForm):
    title = forms.CharField(required=False)
    start_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'])
    end_date = forms.DateField(required=False)

    DEFAULT_START_DATE = datetime.date(2021, 1, 1)
    DEFAULT_END_DATE = get_tomorrow()

    def clean_title(self) -> str | None:
        title = self.cleaned_data.get('title')
        if title == 'all':
            return None

        return title

    def clean_start_date(self) -> str | None:
        start_date = self.cleaned_data.get('start_date')
        if not start_date:
            return self.DEFAULT_START_DATE

        return start_date

    def clean_end_date(self) -> str | None:
        end_date = self.cleaned_data.get('end_date')
        if not end_date:
            return self.DEFAULT_END_DATE

        return end_date
