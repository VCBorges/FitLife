from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View

from ..core import viewsmixins as mixins


class BaseFormView(
    LoginRequiredMixin,
    mixins.BaseFormViewMixin,
    View,
):
    pass


class LoggedOutFormView(
    mixins.BaseFormViewMixin,
    View,
):
    pass


class BaseTemplateView(
    LoginRequiredMixin,
    mixins.BaseContextTemplateViewMixin,
    TemplateView,
):
    pass


class LoggedOutTemplateView(
    mixins.BaseContextTemplateViewMixin,
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = reverse_lazy(settings.LOGIN_REDIRECT_URL)
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
