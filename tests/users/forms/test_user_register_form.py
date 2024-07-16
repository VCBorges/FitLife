from datetime import datetime

from django.urls import reverse

from app.users import forms
from app.users.models import Users

import pytest


@pytest.mark.django_db
def test_to_be_valid_and_create_a_user():
    form = forms.UserRegisterForm(
        data={
            'username': 'test3@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'test',
            'last_name': 'test',
            'birth_date': '1980-01-01',
            'cpf': '52358375098',
        },
    )
    assert form.is_valid() is True
    data = form.save()
    assert data['redirect_url'] == reverse('login_template')
    user = Users.objects.get(email='test3@test.com')
    assert user.email == 'test3@test.com'
    assert user.first_name == 'test'
    assert user.last_name == 'test'
    assert user.birth_date == datetime(1980, 1, 1).date()
    assert user.document == '52358375098'


@pytest.mark.django_db
def test_to_return_login_template_when_form_is_valid():
    form = forms.UserRegisterForm(
        data={
            'username': 'test3@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'test',
            'last_name': 'test',
            'birth_date': '1980-01-01',
            'cpf': '52358375098',
        },
    )
    form.is_valid()

    data = form.save()

    assert data['redirect_url'] == reverse('login_template')
