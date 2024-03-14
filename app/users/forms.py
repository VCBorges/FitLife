from django import forms
from django.urls import reverse

from ..core.forms import BaseForm
from . import utils
from .models import Users

from validate_docbr import CPF


class UserRegisterForm(BaseForm):
    username = forms.EmailField(required=True)  # Email
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    cpf = forms.CharField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if Users.objects.filter(email=username).exists():
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def clean_cpf(self):
        cpf = utils.clean_cpf(self.cleaned_data.get('cpf'))
        if cpf and Users.objects.filter(document=cpf).exists():
            raise forms.ValidationError('CPF is already in use.')
        if not CPF().validate(cpf):
            raise forms.ValidationError('Invalid CPF.')
        return cpf

    # def clean(self) -> dict[str, Any]:
    #     data = super().clean()
    #     if data['password1'] != data['password2']:
    #         raise forms.ValidationError('Passwords do not match.')
    #     return data

    def save(self):
        Users.objects.create_user(
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

    def save(self, user):
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return {
            'redirect_url': reverse('login_template'),
        }


class UpdateUserForm(BaseForm):
    ...
