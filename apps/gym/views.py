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
from apps.gym import dtos, forms, models, ui
from apps.gym.services import WorkoutService

# Create your views here.


class LandingPageTemplateView(LoggedOutTemplateView):
    template_name = 'gym/landing_page.html'


class HomepageTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/homepage.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['context'] = {
            'workouts': ui.workouts_list(
                lookups=dtos.UserWorkoutLookups(user=self.request.user),
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


class CompleteWorkoutTemplateView(AuthDetailTemplateView):
    template_name = 'gym/complete_workout.html'
    model = models.Workouts
    object: models.Workouts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = Language.PT
        context['workout'] = self.object
        context['workout_exercises'] = ui.workout_exercises_form_card(
            workout=self.object,
            language=language,
        )
        return context


class CreateListWorkoutsView(AuthenticatedFormView):
    http_method_names = ['post']

    def post(self, *args, **kwargs) -> JsonResponse:
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


class CreateListWorkoutsHistoryView(AuthenticatedFormView):
    http_method_names = ['post']

    def post(self, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.CompleteWorkoutForm)
        WorkoutService().complete_workout(
            user=self.request.user,
            workout=data.get('workout'),
            exercises=data.get('exercises'),
        )
        return self.get_response(
            status_code=201,
            message='Workout completed successfully',
        )


class DetailDeleteWorkoutHistoryView(AuthenticatedFormView):
    http_method_names = ['delete']
    model = models.WorkoutHistory

    def delete(self, *args, **kwargs) -> JsonResponse:
        WorkoutService().uncomplete_workout(
            workout=self.object,
        )
        return self.get_response(
            status_code=204,
            message='Workout uncompleted successfully',
        )
