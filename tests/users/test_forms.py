from apps.core.exceptions import BaseError
from apps.users import forms

import pytest


@pytest.mark.django_db
def test_UserSignUpForm_to_be_valid():
    form = forms.UserSignUpForm(
        data={
            'email': 'test@test.com',
            'password1': '123qaz123',
            'password2': '123qaz123',
        },
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_UserSignUpForm_to_be_invalid_when_email_already_exists(
    mock_user: dict[str, str],
):
    form = forms.UserSignUpForm(
        data={
            'email': mock_user['email'],
            'password1': '123qaz123',
            'password2': '123qaz123',
        },
    )
    with pytest.raises(BaseError) as exc:
        form.is_valid()

    assert 'email' in exc.value.error_dict
