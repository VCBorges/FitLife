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
def mock_user() -> dict[str, str]:
    email = 'test@test.com'
    password = '123qaz123'
    UserService.create_user(
        data={
            'email': email,
            'password': password,
        }
    )
    return {
        'email': email,
        'password': password,
    }


@pytest.fixture
def existent_user_email() -> str:
    email = 'test@test.com'
    password = '123qaz123'
    UserService.create_user(
        data={
            'email': email,
            'password': password,
        }
    )
    return email


@pytest.fixture
def user():
    email = 'test@test.com'
    password = '123qaz123'
    user = UserService.create_user(
        data={
            'email': email,
            'password': password,
        }
    )
    return user


@pytest.fixture
def authenticated_client(user: Users) -> Client:
    client = Client()
    client.login(email=user.email, password='123qaz123')
    return client


@pytest.fixture
def client():
    return Client()
