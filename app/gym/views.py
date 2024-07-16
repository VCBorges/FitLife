from django.urls import reverse

from app.core.views import (
    AuthenticatedFormView,
    AuthenticatedTemplateView,
)
from app.gym import forms, presenters


class CreateWorkoutTemplateView(AuthenticatedTemplateView):
    title = 'Criar Treino'
    bundle = 'createWorkout-bundle.js'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context']['endpoints']['createWorkout'] = reverse('create_workout')
        context['context']['selectOptions'] = {
            'exercises': presenters.exercises_select_field_options(),
        }
        context['context']['data'] = {
            'user_workouts': presenters.user_workouts_list(
                user=self.request.user,
                order_by=['-created_at'],
                # page_size=
            )
        }
        return context


class CreateWorkoutView(AuthenticatedFormView):
    form_class = forms.CreateWorkoutForm


class UpdateWorkoutView(AuthenticatedFormView):
    form_class = forms.UpdateWorkoutForm
