from typing import Any

from src.core.typed import BaseFormType
from src.core.views import (
    AuthenticatedFormView,
    LoggedOutFormView,
    LoggedOutTemplateView,
)
from src.users import forms


class UserLoginTemplateView(LoggedOutTemplateView):
    template_name = 'users/login.html'


class UserLoginView(LoggedOutFormView):
    http_method_names = ['post']
    form_class = forms.UserLoginForm

    def process(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any] | None:
        return


class UserLogoutView(AuthenticatedFormView):
    form_class = forms.UserLogoutForm

    def process(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any] | None:
        return


class UserSignUpTemplateView(LoggedOutTemplateView):
    template_name = 'users/signup.html'

    def process(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any] | None:
        return


class UserSignUpView(LoggedOutFormView):
    form_class = forms.UserSignUpForm

    def process(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any] | None:
        return


class UserUpdateView(LoggedOutFormView):
    form_class = forms.UserUpdateView

    def process(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any] | None:
        return


class EmailVerificationView(LoggedOutFormView):
    form_class = forms.EmailVerificationForm

    def process(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any] | None:
        return
