from django.test import Client
from django.urls import reverse

from apps.users.models import Users

import pytest


@pytest.mark.django_db
def test_UserLoginView_to_return_status_code_200_when_form_is_valid():
    Users.objects.create_user(
        email='test@test.com',
        password='123qaz123',
    )

    client = Client()
    url = reverse('login')
    response = client.post(
        path=url,
        data={
            'login': 'test@test.com',
            'password': '123qaz123',
        },
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_UserLoginView_to_have_redirect_url_in_reponse_when_form_is_valid():
    Users.objects.create_user(
        email='test@test.com',
        password='123qaz123',
    )

    client = Client()
    url = reverse('login')
    response = client.post(
        path=url,
        data={
            'login': 'test@test.com',
            'password': '123qaz123',
        },
    )
    assert 'redirect_url' in response.json()


@pytest.mark.django_db
def test_UserSignUpView_to_create_a_new_user():
    client = Client()
    url = reverse('signup')
    client.post(
        path=url,
        data={
            'email': 'testcreateuser@test.com',
            'password1': '123qaz123',
            'password2': '123qaz123',
        },
    )
    assert Users.objects.filter(email='testcreateuser@test.com').exists()
