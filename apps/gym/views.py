from typing import Any

from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse

from apps.core.constants import Language
from apps.core.views import (
    AuthDetailTemplateView,
    AuthenticatedFormView,
    AuthenticatedTemplateView,
    LoggedOutTemplateView,
)
from apps.gym import forms, models, ui
from apps.gym.services import WorkoutService

# Create your views here.
from rich import print


class LandingPageTemplateView(LoggedOutTemplateView):
    template_name = 'gym/landing_page.html'


class HomepageTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/homepage.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['context'] = {
            'workouts': ui.workouts_list(
                user=self.request.user,
                language=Language.PT,
            ),
        }
        return context


class CreateWorkoutTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/create_workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = Language.PT
        context['context'] = {
            'muscles': ui.muscles_select_input_options(
                language=language,
            ),
            'equipments': ui.equipments_select_input_options(
                language=language,
            ),
            'exercises': ui.exercises_select_input_options(
                language=language,
            ),
        }
        return context


class UpdateWorkoutTemplateView(AuthDetailTemplateView):
    template_name = 'gym/update_workout.html'
    model = models.Workouts
    object: models.Workouts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = Language.PT
        context['context'] = {
            'muscles': ui.muscles_select_input_options(
                language=language,
            ),
            'equipments': ui.equipments_select_input_options(
                language=language,
            ),
            'exercises': ui.exercises_select_input_options(
                language=language,
            ),
        }
        context['workout'] = self.object
        context['workout_exercises'] = ui.workout_exercises_form_card(
            workout=self.object,
            language=language,
        )
        return context


class CreateListWorkoutsView(AuthenticatedFormView):
    http_method_names = ['post']

    def post(self, *args, **kwargs) -> JsonResponse:
        print(f'{self.data = }')
        data = self.get_cleaned_data(forms.CreateWorkoutForm)
        workout = WorkoutService().create_workout(
            user=self.request.user,
            title=data['title'],
            description=data.get('description'),
            exercises=data.get('exercises'),
        )
        return self.get_response(
            status_code=201,
            message='Workout created successfully',
            data={'workout': workout.id},
        )


class UpdateDetailDeleteWorkoutView(AuthenticatedFormView):
    http_method_names = ['put', 'delete']
    model = models.Workouts

    def put(self, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.UpdateWorkoutForm)
        WorkoutService().update_workout(
            workout=self.object,
            title=data.get('title'),
            description=data.get('description'),
            exercises=data.get('exercises'),
        )

    def delete(self, *args, **kwargs) -> dict[str, Any]:
        WorkoutService.delete_workout(
            workout=self.object,
        )
