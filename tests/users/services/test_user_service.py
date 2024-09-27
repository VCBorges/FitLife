from django import forms

from apps.users.models import Users
from apps.users.services import UserService

import pytest
from allauth.account.models import EmailAddress


@pytest.mark.django_db
def test_create_user_to_create_a_new_user():
    UserService.create_user(
        data={
            'email': 'testcreateuser@test.com',
            'password': 'testpassword',
            'first_name': 'Test',
        }
    )
    assert Users.objects.filter(email='testcreateuser@test.com').exists()


@pytest.mark.django_db
def test_create_user_to_create_a_email_address():
    UserService.create_user(
        data={
            'email': 'testcreateuser@test.com',
            'password': 'testpassword',
            'first_name': 'Test',
        }
    )

    assert EmailAddress.objects.filter(email='testcreateuser@test.com').exists()


@pytest.mark.django_db
def test_create_user_to_create_a_non_verified_email_address():
    UserService.create_user(
        data={
            'email': 'testcreateuser@test.com',
            'password': 'testpassword',
            'first_name': 'Test',
        }
    )

    address = EmailAddress.objects.filter(email='testcreateuser@test.com').first()

    assert not address.verified


@pytest.mark.django_db
def test_create_user_to_create_a_primary_email_address():
    UserService.create_user(
        data={
            'email': 'testcreateuser@test.com',
            'password': 'testpassword',
            'first_name': 'Test',
        }
    )

    address = EmailAddress.objects.filter(email='testcreateuser@test.com').first()

    assert address.primary


@pytest.mark.django_db
def test_create_user_to_raise_error_when_email_already_exists(existent_user_email: str):
    with pytest.raises(forms.ValidationError) as exc:
        UserService.create_user(
            data={
                'email': existent_user_email,
                'password': 'testpassword',
                'first_name': 'Test',
            }
        )

    assert exc.value.messages[0]
