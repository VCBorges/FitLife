from apps.core.exceptions import BaseAPIError
from apps.users import forms
from apps.users.models import Users

import pytest


@pytest.mark.django_db
def test_UserSignUpForm_to_be_valid():
    form = forms.UserSignUpForm(
        data={
            'first_name': 'Test',
            'email': 'test@test.com',
            'password1': '123qaz123',
            'password2': '123qaz123',
        },
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_UserSignUpForm_to_be_invalid_when_email_already_exists(
    user: Users,
):
    form = forms.UserSignUpForm(
        data={
            'first_name': 'Test',
            'email': user.email,
            'password1': '123qaz123',
            'password2': '123qaz123',
        },
    )
    with pytest.raises(BaseAPIError) as exc:
        form.is_valid()

    assert 'email' in exc.value.error_dict
