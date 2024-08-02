from src.core.forms import BaseForm

# from src.core import form_fiel
from allauth.account.forms import LoginForm


class UserLoginForm(LoginForm):
    ...


class UserLogoutForm(BaseForm):
    ...


class UserSignUpForm(BaseForm):
    ...


class UserUpdateView(BaseForm):
    ...


class EmailVerificationForm(BaseForm):
    ...
