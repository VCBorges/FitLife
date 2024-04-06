from typing import Any, TypeVar

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View

from app.core import viewsmixins as mixins
from app.core.protocols import AuthenticatedRequest

T = TypeVar('T', bound=models.Model)


class AuthenticatedFormView(
    LoginRequiredMixin,
    mixins.BaseFormViewMixin,
    View,
):
    request: AuthenticatedRequest


class AuthenticatedUpdateFormView(
    LoginRequiredMixin,
    mixins.BaseUpdateFormViewMixin,
    View,
):
    request: AuthenticatedRequest


class LoggedOutFormView(
    mixins.BaseFormViewMixin,
    View,
):
    pass


class AuthenticatedTemplateView(
    LoginRequiredMixin,
    mixins.BaseContextTemplateViewMixin,
    TemplateView,
):
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
    mixins.BaseContextTemplateViewMixin,
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = reverse_lazy(settings.LOGIN_REDIRECT_URL)
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
