from django.urls import path

from apps.gym import views

templates_urls = [
    path(
        route='',
        view=views.LandingPageTemplateView.as_view(),
        name='landing_page_template',
    ),
    path(
        route='home/',
        view=views.HomepageTemplateView.as_view(),
        name='homepage_template',
    ),
    path(
        route='workout/create/',
        view=views.CreateWorkoutTemplateView.as_view(),
        name='create_workout_template',
    ),
]

api_urls = [
    path(
        route='workout/',
        view=views.CreateListWorkoutsView.as_view(),
        name='create_list_workouts',
    ),
]

urlpatterns = templates_urls + api_urls
