from django.urls import path

from . import views

workout_urlpatterns = [
    path(
        'workouts/',
        views.WorkoutTemplateView.as_view(),
        name='workout_template',
    ),
    path(
        'workouts/create/',
        views.CreateWorkoutView.as_view(),
        name='create_workout',
    ),
    # path(
    #     'workouts/<uuid:workout_id>/exercise/create/',
    #     views.AddExerciseToWorkoutView.as_view(),
    #     name='add_exercise_to_workout',
    # ),
    # path(
    #     'workouts/<uuid:workout_id>/update/',
    #     views.UpdateWorkoutView.as_view(),
    #     name='update_workout',
    # ),
]

urlpatterns = []
urlpatterns += workout_urlpatterns
