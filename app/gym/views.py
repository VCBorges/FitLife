from ..core.views import (
    AuthenticatedTemplateView,
)


class WorkoutTemplateView(AuthenticatedTemplateView):
    template_name = 'gym/workouts.html'
