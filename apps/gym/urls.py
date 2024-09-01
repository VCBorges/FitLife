from django.urls import path

from apps.gym import views

templates_urls = [
    path('', views.LandingPageTemplateView.as_view(), name='landing_page_template'),
    path('home/', views.HomepageTemplateView.as_view(), name='homepage_template'),
    path(
        'workout/create/',
        views.CreateWorkoutTemplateView.as_view(),
        name='create_workout_template',
    ),
]

api_urls = [
    path(
        'workout/', views.CreateListWorkoutsView.as_view(), name='create_list_workouts'
    ),
]

urlpatterns = templates_urls + api_urls
