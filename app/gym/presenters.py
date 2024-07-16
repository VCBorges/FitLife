from django.core.paginator import Paginator
from django.db.models import QuerySet

from app.core.utils.presenters import get_model_select_field_options
from app.gym import models
from app.gym.repositories.workout_history import WorkoutsHistoryRepository
from app.gym.repositories.workouts import WorkoutsRepository
from app.users.models import Users


def exercises_select_field_options() -> list[models.Exercises]:
    return get_model_select_field_options(
        model=models.Exercises,
    )


# def get_user_workouts(
#     user: Users,
#     # limit: int ,
#     **lookup_filters,
# ) -> list[dict]:
#     workouts = WorkoutsRepository.filter_by_user(
#         user=user,
#         prefetch_related=[
#             'workout_exercises__exercise__primary_muscle',
#             'workout_exercises__exercise__secondary_muscle',
#         ],
#         **lookup_filters,
#     )
#     paginator = Paginator(workouts, 5)

#     return [
#         {
#             'id': workout.uuid,
#             'name': workout.name,
#             'description': workout.description,
#             'created_at': workout.created_at,
#             'exercises': [
#                 {
#                     'uuid': workout_exercise.uuid,
#                     'name': workout_exercise.exercise.name,
#                     'repetitions': workout_exercise.repetitions,
#                     'sets': workout_exercise.sets,
#                     'primary_muscle': workout_exercise.exercise.primary_muscle.name,
#                     'secondary_muscle': workout_exercise.exercise.secondary_muscle.name,
#                 }
#                 for workout_exercise in workout.exercises.all()
#             ],
#         }
#         for workout in workouts
#     ]


def user_workouts_list(
    user: Users,
    page_size: int = 5,
    page_number: int = 1,
    order_by: list[str] | None = None,
    **lookup_filters,
) -> list[dict]:
    queryset = WorkoutsRepository.filter_by_user(
        user=user,
        prefetch_related=[
            'workout_exercises',
        ],
        order_by=order_by,
        **lookup_filters,
    )
    paginator = Paginator(
        object_list=queryset,
        per_page=page_size,
    )
    page = paginator.get_page(page_number)
    workouts: QuerySet[models.Workouts] = page.object_list
    return [
        {
            'id': workout.uuid,
            'name': workout.title,
            'description': workout.description,
            'created_by': workout.created_by,
            'created_at': workout.created_at,
            'exercises_count': len(workout.exercises.all()),
        }
        for workout in workouts
    ]


def user_workout_details() -> list[dict]:
    pass


def user_workout_history_list() -> list[dict]:
    pass


def user_workout_history_details() -> list[dict]:
    pass


# def user_workouts_pagination(
#     user: Users,
#     page_size: int = 5,
#     page_number: int = 1,
#     order_by: list[str] | None = None,
#     **lookup_filters,
# ) -> list[dict]:
#     queryset = WorkoutsRepository.filter_by_user(
#         user=user,
#         prefetch_related=[
#             'workout_exercises__exercise__primary_muscle',
#             'workout_exercises__exercise__secondary_muscle',
#         ],
#         order_by=order_by,
#         **lookup_filters,
#     )
#     paginator = Paginator(
#         object_list=queryset,
#         per_page=page_size,
#     )
#     page = paginator.get_page(page_number)
#     workouts: QuerySet[models.Workouts] = page.object_list
#     return [
#         {
#             'id': workout.uuid,
#             'name': workout.name,
#             'description': workout.description,
#             'created_at': workout.created_at,
#             'exercises': [
#                 {
#                     'uuid': workout_exercise.uuid,
#                     'name': workout_exercise.exercise.name,
#                     'repetitions': workout_exercise.repetitions,
#                     'sets': workout_exercise.sets,
#                     'primary_muscle': workout_exercise.exercise.primary_muscle.name,
#                     'secondary_muscle': workout_exercise.exercise.secondary_muscle.name,
#                 }
#                 for workout_exercise in workout.exercises.all()
#             ],
#         }
#         for workout in workouts
#     ]


def get_completed_workouts_by_user(
    user: Users,
    **lookup_filters,
) -> list[dict]:
    workouts = WorkoutsHistoryRepository.filter_by_user(
        user=user,
        prefetch_related=[
            'workout_exercises__exercises',
            'workout_exercises__exercises',
        ],
        **lookup_filters,
    )
    return [
        {
            'uuid': workout.uuid,
            'name': workout.title,
            'description': workout.description,
            'created_at': workout.created_at,
            'exercises': [
                {
                    'uuid': workout_exercise.uuid,
                    'name': workout_exercise.exercise.name,
                    'repetitions': workout_exercise.repetitions,
                    'sets': workout_exercise.sets,
                    'primary_muscle': workout_exercise.exercise.primary_muscle.name,
                    'secondary_muscle': workout_exercise.exercise.secondary_muscle.name,
                }
                for workout_exercise in workout.exercises.all()
            ],
        }
        for workout in workouts
    ]
