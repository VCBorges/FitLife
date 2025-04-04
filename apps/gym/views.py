from typing import Any

from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy

from apps.core.utils import get_tomorrow
from apps.core.views import (
    AuthDetailTemplateView,
    AuthenticatedAPIView,
    AuthenticatedTemplateView,
    LoggedOutTemplateView,
)
from apps.gym import dtos, forms, models, selectors
from apps.gym.services import WorkoutService


class LandingPageTemplateView(LoggedOutTemplateView):
    template_name = 'gym/landing_page.html'


class HomepageTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/homepage.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['context'] = {
            'workouts': selectors.workouts_list(
                lookups=dtos.UserWorkoutLookups(user=self.request.user),
                language=self.language,
            ),
        }
        return context


class CreateWorkoutTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/create_workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['context'] = {
            'muscles': selectors.muscles_select_input_options(
                language=self.language,
            ),
            'equipments': selectors.equipments_select_input_options(
                language=self.language,
            ),
            'exercises': selectors.exercises_select_input_options(
                language=self.language,
            ),
        }
        return context


class UpdateWorkoutTemplateView(AuthDetailTemplateView):
    template_name = 'gym/update_workout.html'
    model = models.Workout
    object: models.Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context'] = {
            'muscles': selectors.muscles_select_input_options(
                language=self.language,
            ),
            'equipments': selectors.equipments_select_input_options(
                language=self.language,
            ),
            'exercises': selectors.exercises_select_input_options(
                language=self.language,
            ),
        }
        context['workout'] = self.object
        context['workout_exercises'] = selectors.workout_exercises_form_card(
            workout=self.object,
            language=self.language,
        )
        return context


class CompleteWorkoutTemplateView(AuthDetailTemplateView):
    template_name = 'gym/complete_workout.html'
    model = models.Workout
    object: models.Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout'] = self.object
        context['workout_exercises'] = selectors.workout_exercises_form_card(
            workout=self.object,
            language=self.language,
        )
        return context


class WorkoutHistoriesTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/workout_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout_histories'] = selectors.workout_history_list(
            lookups=dtos.UserWorkoutLookups(user=self.request.user),
            language=self.language,
        )
        context['workout_histories_select_options'] = (
            selectors.workout_history_select_filter_options()
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
            creator=self.request.user,
            title=data['title'],
            description=data.get('description'),
            exercises=data.get('exercises'),
        )
        return self.render_to_json(
            data={
                'workout': workout.id,
                'redirect_url': reverse_lazy('homepage_template'),
            },
            status_code=201,
        )

    def get(self, *args, **kwargs) -> dict[str, Any]:
        workouts = selectors.workouts_list(
            lookups=dtos.UserWorkoutLookups(
                user=self.request.user,
                title__icontains=self.data['query'],
            ),
            language=self.language,
        )

        return self.render_to_template(
            template='gym/htmx/_workout_list_item.html',
            context={'workouts': workouts},
        )


class UpdateDetailDeleteWorkoutView(AuthenticatedAPIView):
    http_method_names = ['put', 'delete']
    model = models.Workout

    def put(self, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.UpdateWorkoutForm)
        WorkoutService().update_workout(
            workout=self.object,
            title=data['title'],
            description=data['description'],
            exercises=data['exercises'],
        )
        return self.render_to_json(
            data={
                'redirect_url': reverse_lazy('homepage_template'),
            },
            status_code=200,
        )

    def delete(self, *args, **kwargs) -> dict[str, Any]:
        WorkoutService().delete_workout(
            workout=self.object,
        )
        return self.render_to_json(status_code=200)


class CreateListWorkoutHistoriesView(AuthenticatedAPIView):
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
            data={
                'redirect_url': reverse_lazy('workout_history_template'),
            },
        )

    def get(self, *args, **kwargs) -> dict[str, Any]:
        data = self.get_cleaned_data(forms.FilterWorkoutHistoriesForm)
        workout_histories = selectors.workout_history_list(
            lookups=dtos.UserWorkoutHistoryLookups(
                user=self.request.user,
                title=data.get('title'),
                completed_at__range=(
                    data.get('start_date'),
                    data.get('end_date', get_tomorrow()),
                ),
            ),
            language=self.language,
        )
        return self.render_to_template(
            template='gym/htmx/_workout_history_list_items.html',
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
