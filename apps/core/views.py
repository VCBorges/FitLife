from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View

from apps.core import viewsmixins
from apps.core.typed import AuthenticatedRequest


class AuthenticatedFormView(
    LoginRequiredMixin,
    viewsmixins.BaseFormViewMixin,
    View,
):
    request: AuthenticatedRequest


class LoggedOutFormView(
    viewsmixins.CsrfExemptMixin,
    viewsmixins.BaseFormViewMixin,
    View,
):
    pass


class AuthenticatedTemplateView(
    LoginRequiredMixin,
    viewsmixins.BaseTemplateViewContextMixin,
    TemplateView,
):
    request: AuthenticatedRequest

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class LoggedOutTemplateView(
    viewsmixins.BaseTemplateViewContextMixin,
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
