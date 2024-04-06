from django.urls import reverse

from app.core.views import (
    AuthenticatedFormView,
    AuthenticatedTemplateView,
    AuthenticatedUpdateFormView,
)
from app.gym import forms
from app.gym.services.exercises import get_exercises_select_field_options


class WorkoutTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/workouts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context']['endpoints']['createWorkout'] = reverse('create_workout')
        context['context']['selectOptions'] = {
            'exercises': get_exercises_select_field_options(),
        }
        return context


class CreateWorkoutView(AuthenticatedFormView):
    form_class = forms.CreateWorkoutForm


class AddExerciseToWorkoutView(AuthenticatedUpdateFormView):
    form_class = ...


class UpdateWorkoutView(AuthenticatedFormView):
    form_class = forms.UpdateWorkoutForm

