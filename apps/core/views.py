from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView

from apps.core import viewsmixins
from apps.core.typed import AuthenticatedRequest, DjangoModelType


class AuthenticatedAPIView(
    LoginRequiredMixin,
    viewsmixins.BaseAPIView,
    View,
):
    request: AuthenticatedRequest


class LoggedOutAPIView(
    viewsmixins.CsrfExemptMixin,
    viewsmixins.BaseAPIView,
    View,
):
    pass


class AuthenticatedTemplateView(
    LoginRequiredMixin,
    viewsmixins.BaseTemplateContextMixin,
    TemplateView,
):
    request: AuthenticatedRequest

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class AuthDetailTemplateView(
    LoginRequiredMixin,
    viewsmixins.BaseTemplateContextMixin,
    DetailView,
):
    model: DjangoModelType


class LoggedOutTemplateView(
    viewsmixins.BaseTemplateContextMixin,
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     redirect_to = reverse_lazy(settings.LOGIN_REDIRECT_URL)
        #     return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
