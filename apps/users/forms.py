from typing import override

from django import forms

from apps.core.exceptions import FormValidationError
from apps.core.forms import BaseForm

from allauth.account.forms import LoginForm, SignupForm
from allauth.account.models import EmailAddress


class UserLoginForm(LoginForm):
    @override
    def is_valid(self, *, raise_exception: bool = True) -> bool:
        valid = super().is_valid()

        if not valid and raise_exception:
            raise FormValidationError(self.errors)

        return valid


class UserSignUpForm(BaseForm, SignupForm):
    first_name = forms.CharField(required=True)

    normalized_fields_mapping = {
        'password1': 'password',
    }

    def clean_email(self):
        email = super().clean_email()
        if EmailAddress.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email


class UserUpdateView(BaseForm):
    ...


class EmailVerificationForm(BaseForm):
    ...
