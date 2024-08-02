from django.http import HttpRequest, JsonResponse

from src.core.views import AuthenticatedFormView
from src.gym import forms

# Create your views here.
from rich import print


class CreateListWorkoutView(AuthenticatedFormView):
    http_method_names = ['post', 'get']

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        data = self.get_cleaned_data(forms.CreateWorkoutExerciseForm)
        print(f'{data = }')
        return {'test': 'response'}

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        print(f'{request = }')
        return {'get': request.GET}
