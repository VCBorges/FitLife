from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View

from app.core.mixins import views
from app.core.protocols import AuthenticatedRequest


class AuthenticatedFormView(
    LoginRequiredMixin,
    views.BaseFormViewMixin,
    View,
):
    request: AuthenticatedRequest


class AuthenticatedInstanceFormView(
    LoginRequiredMixin,
    views.BaseInstanceFormViewMixin,
    View,
):
    request: AuthenticatedRequest


class LoggedOutFormView(
    views.BaseFormViewMixin,
    View,
):
    pass


class AuthenticatedTemplateView(
    LoginRequiredMixin,
    views.BaseTemplateViewMixin,
    TemplateView,
):
    request: AuthenticatedRequest

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['context'] = {
            'endpoints': {
                'templates': {
                    'workouts': reverse('workout_template'),
                    'user': reverse('user_template'),
                },
                'logout': reverse('logout'),
            },
            'images': {
                'fitLifeLogo': static('public/images/fitlife_logo.jpeg'),
            },
            'data': {},
        }
        return context


class LoggedOutTemplateView(
    views.BaseTemplateViewMixin,
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = reverse_lazy(settings.LOGIN_REDIRECT_URL)
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['context'] = {
            'endpoints': {
                'templates': {},
            },
            'images': {
                'fitLifeLogo': static('public/images/fitlife_logo.jpeg'),
            },
            'data': {},
        }
        return context
