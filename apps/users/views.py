from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from apps.core.views import (
    AuthenticatedFormView,
    LoggedOutFormView,
    LoggedOutTemplateView,
)
from apps.users import forms
from apps.users.services import UserService

from allauth.account.mixins import LogoutFunctionalityMixin


class UserLoginTemplateView(LoggedOutTemplateView):
    template_name = 'users/login.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy(settings.LOGIN_REDIRECT_URL))

        return super().dispatch(*args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)


class UserLoginView(LoggedOutFormView):
    http_method_names = ['post']

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> Any:
        form: forms.UserLoginForm = self.get_form(forms.UserLoginForm)
        form.is_valid()
        form.login(self.request)
        return self.get_response(
            data={
                'redirect_url': reverse_lazy(settings.LOGIN_REDIRECT_URL),
            },
        )


class UserLogoutView(AuthenticatedFormView, LogoutFunctionalityMixin):
    http_method_names = ['post']

    def post(self, *args, **kwargs) -> dict[str, Any]:
        if self.request.user.is_authenticated:
            self.logout()
        return self.get_response(
            status_code=200,
            data={
                'redirect_url': reverse_lazy(settings.LOGOUT_REDIRECT_URL),
            },
        )


class UserSignUpTemplateView(LoggedOutTemplateView):
    template_name = 'users/signup.html'


class UserSignUpView(LoggedOutFormView):
    http_method_names = ['post']

    def post(self, *args, **kwargs) -> dict[str, Any]:
        data = self.get_cleaned_data(forms.UserSignUpForm)
        UserService.create_user(data)
        return self.get_response(
            status_code=302,
            data={
                'redirect_url': '',
            },
        )


class UserUpdateView(LoggedOutFormView):
    form_class = forms.UserUpdateView


class EmailVerificationView(LoggedOutFormView):
    form_class = forms.EmailVerificationForm
