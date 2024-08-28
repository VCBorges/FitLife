from django.http import JsonResponse

from apps.core.views import (
    AuthenticatedFormView,
    AuthenticatedTemplateView,
    LoggedOutTemplateView,
)
from apps.gym import forms
from apps.gym.services import WorkoutService

# Create your views here.
from rich import print


class LandingPageTemplateView(LoggedOutTemplateView):
    template_name = 'gym/landing_page.html'


class HomepageTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/homepage.html'


class CreateWorkoutTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/create_workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateWorkoutTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/update_workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateListWorkoutsView(AuthenticatedFormView):
    http_method_names = ['post', 'get']

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

    def get(self, *args, **kwargs) -> JsonResponse:
        print(f'{self.request = }')
        return {'get': self.request.GET}
