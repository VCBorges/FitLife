from django.contrib.sessions.backends.db import SessionStore
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client
from django.test.client import RequestFactory

from apps.users.models import Users
from apps.users.services import UserService

import pytest


@pytest.fixture
def mock_request() -> WSGIRequest:
    request = RequestFactory().post('/')
    request.user = None
    request.session = SessionStore()
    request.session.save()
    return request


@pytest.fixture
def user_password() -> str:
    return '123qaz123'


@pytest.fixture
def user(user_password: str):
    email = 'test@test.com'
    first_name = 'Test'
    user = UserService.create_user(
        data={
            'email': email,
            'password': user_password,
            'first_name': first_name,
        }
    )
    return user


@pytest.fixture
def existent_user_email(user: Users) -> str:
    return user.email


@pytest.fixture
def authenticated_client(
    user: Users,
    user_password: str,
) -> Client:
    client = Client()
    client.login(
        email=user.email,
        password=user_password,
    )
    return client


@pytest.fixture
def client():
    return Client()
