from django.core.paginator import Paginator
from django.db.models import Prefetch

from apps.gym import models, typed


class WorkoutSelector:
    @staticmethod
    def list_workouts_history(
        user: models.Users,
        *,
        page: int = 1,
        per_page: int = 10,
        lookups: typed.ListWorkoutsHistoryLookups = {},
        order_by: list[str] = ['-created_at'],
    ):
        exercises = models.WorkoutHistoryExercises.objects.all()
        workouts = models.WorkoutHistory.objects.prefetch_related(
            Prefetch(
                'workout_history_exercises',
                queryset=exercises,
                to_attr='workout_history_exercises',
            ),
        )
        workouts = workouts.filter(
            user=user,
            **lookups,
        )
        workouts = workouts.order_by(*order_by)
        # workouts = models.WorkoutHistory.objects.filter(
        #     user=user)
        paginator = Paginator(
            object_list=workouts,
            per_page=per_page,
        )
        return paginator.get_page(page).object_list
