from django import forms
from django.urls import reverse

from ..core.forms import BaseForm
from .models import Users


class UserRegisterForm(BaseForm):
    username = forms.EmailField(required=True)  # Email
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if Users.objects.filter(email=username).exists():
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self):
        Users.objects.create_user(
            email=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            birth_date=self.cleaned_data['birth_date'],
        )
        return {
            'redirect_url': reverse('login_template'),
        }
