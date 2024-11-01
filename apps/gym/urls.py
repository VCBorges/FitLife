from django.urls import path

from apps.gym import views

templates_urls = [
    # path(
    #     route='',
    #     view=views.LandingPageTemplateView.as_view(),
    #     name='landing_page_template',
    # ),
    path(
        route='',
        view=views.HomepageTemplateView.as_view(),
        name='homepage_template',
    ),
    path(
        route='workouts/create/',
        view=views.CreateWorkoutTemplateView.as_view(),
        name='create_workout_template',
    ),
    path(
        route='workouts/update/<uuid:pk>/',
        view=views.UpdateWorkoutTemplateView.as_view(),
        name='update_workout_template',
    ),
    path(
        route='workouts/complete/<uuid:pk>/',
        view=views.CompleteWorkoutTemplateView.as_view(),
        name='complete_workout_template',
    ),
    path(
        route='workouts/history/',
        view=views.WorkoutHistoriesTemplateView.as_view(),
        name='workout_history_template',
    ),
]

api_urls = [
    path(
        route='workouts/',
        view=views.CreateListWorkoutsView.as_view(),
        name='create_list_workouts',
    ),
    path(
        route='workouts/<uuid:pk>/',
        view=views.UpdateDetailDeleteWorkoutView.as_view(),
        name='update_detail_delete_workouts',
    ),
    path(
        route='workout-histories/',
        view=views.CreateListWorkoutHistoriesView.as_view(),
        name='create_list_workouts_history',
    ),
    # path(
    #     route='workouts/<uuid:pk>/uncomplete/',
    #     view=views.CompleteWorkoutView.as_view(),
    #     name='create_list_workouts_history',
    # ),
]

urlpatterns = templates_urls + api_urls
