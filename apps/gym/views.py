from typing import Any

from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse

from apps.core.constants import Language
from apps.core.views import (
    AuthDetailTemplateView,
    AuthenticatedAPIView,
    AuthenticatedTemplateView,
    LoggedOutTemplateView,
)
from apps.gym import dtos, forms, models, ui
from apps.gym.services import WorkoutService


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


class WorkoutHistoriesTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/workout_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = Language.PT
        context['workout_histories'] = ui.workout_history_list(
            lookups=dtos.UserWorkoutLookups(user=self.request.user),
            language=language,
        )
        return context


class CreateListWorkoutsView(AuthenticatedAPIView):
    http_method_names = [
        'post',
        'get',
    ]

    def post(self, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.CreateWorkoutForm)
        workout = WorkoutService().create_workout(
            user=self.request.user,
            title=data['title'],
            description=data.get('description'),
            exercises=data.get('exercises'),
        )
        return self.render_to_json(
            data={'workout': workout.id},
            status_code=201,
        )

    def get(self, *args, **kwargs) -> dict[str, Any]:
        language = Language.PT
        workouts = ui.workouts_list(
            lookups=dtos.UserWorkoutLookups(
                user=self.request.user,
                title__icontains=self.data['query'],
            ),
            language=language,
        )

        return self.render_to_template(
            template='gym/htmx/_workout_list_item.html',
            context={'workouts': workouts},
        )


class UpdateDetailDeleteWorkoutView(AuthenticatedAPIView):
    http_method_names = ['put', 'delete']
    model = models.Workouts

    def put(self, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.UpdateWorkoutForm)
        WorkoutService().update_workout(
            workout=self.object,
            title=data['title'],
            description=data['description'],
            exercises=data['exercises'],
        )
        return self.render_to_json(status_code=200)

    def delete(self, *args, **kwargs) -> dict[str, Any]:
        WorkoutService().delete_workout(
            workout=self.object,
        )
        return self.render_to_json(status_code=204)


class CompleteWorkoutView(AuthenticatedAPIView):
    http_method_names = ['post', 'delete']

    model = models.Workouts
    object: models.Workouts

    def post(self, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.CompleteWorkoutForm)
        WorkoutService().complete_workout(
            user=self.request.user,
            workout=self.object,
            exercises=data['exercises'],
        )
        return self.render_to_json(
            status_code=201,
        )


class CreateListWorkoutHistoryView(AuthenticatedAPIView):
    http_method_names = [
        'post',
        'get',
    ]

    def post(self, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.CreateWorkoutHistoryForm)
        WorkoutService().complete_workout(
            user=self.request.user,
            workout=data['workout'],
            exercises=data['exercises'],
        )
        return self.render_to_json(
            status_code=201,
        )

    def get(self, *args, **kwargs) -> dict[str, Any]:
        language = Language.PT
        workout_histories = ui.workout_history_list(
            lookups=dtos.UserWorkoutHistoryLookups(
                user=self.request.user,
                workout__title__icontains=self.data['query'],
            ),
            language=language,
        )

        return self.render_to_template(
            template='gym/htmx/_workout_history_list_item.html',
            context={'workout_histories': workout_histories},
        )


class UncompleteWorkoutView(AuthenticatedAPIView):
    http_method_names = ['delete']

    model = models.WorkoutHistory

    def delete(self, *args, **kwargs) -> JsonResponse:
        WorkoutService().uncomplete_workout(
            workout=self.object,
        )
        return self.render_to_json(
            status_code=204,
        )
