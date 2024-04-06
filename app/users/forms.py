from datetime import datetime

from django import forms
from django.urls import reverse

from app.users.services.users import create_user

from ..core.forms import BaseForm
from ..core.utils.date import get_current_year
from ..core.utils.string import has_special_characters
from . import utils
from .models import Users

from validate_docbr import CPF


class UserRegisterForm(BaseForm):
    username = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    cpf = forms.CharField(required=True)

    def clean_first_name(self) -> str:
        first_name = self.cleaned_data['first_name']
        if has_special_characters(first_name):
            raise forms.ValidationError('Caracteres especiais não são permitidos.')
        return first_name

    def clean_last_name(self) -> str:
        last_name = self.cleaned_data['last_name']
        if has_special_characters(last_name):
            raise forms.ValidationError('Caracteres especiais não são permitidos.')
        return last_name

    def clean_username(self) -> str:
        username = self.cleaned_data['username']
        if Users.objects.filter(email=username).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return username

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def clean_cpf(self) -> str:
        cpf = utils.clean_cpf(self.cleaned_data.get('cpf'))
        if not CPF().validate(cpf):
            raise forms.ValidationError('CPF inválido.')
        if cpf and Users.objects.filter(document=cpf).exists():
            raise forms.ValidationError('Este CPF já está em uso.')
        return cpf

    def clean_birth_date(self) -> datetime:
        birth_date = self.cleaned_data.get('birth_date')
        if get_current_year() - birth_date.year < 14:
            raise forms.ValidationError('A idade mínima é de 14 anos.')
        return birth_date

    def save(self) -> dict[str, str]:
        create_user(
            email=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            birth_date=self.cleaned_data['birth_date'],
            document=self.cleaned_data['cpf'],
        )
        return {
            'redirect_url': reverse('login_template'),
        }


class UpdatePasswordForm(BaseForm):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self, user: Users) -> dict[str, str]:
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return {
            'redirect_url': reverse('login_template'),
        }


class UpdateUserForm(BaseForm):
    ...
