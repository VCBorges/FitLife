from django.urls import path

from . import views

urlpatterns = [
    path(
        'workouts/',
        views.WorkoutTemplateView.as_view(),
        name='workout_template',
    ),
]
