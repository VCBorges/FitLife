from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_CreateListWorkoutsView_to_return_status_code_201_when_user_is_authenticated(
    authenticated_client: Client,
):
    url = reverse('create_list_workouts')
    response = authenticated_client.post(
        path=url,
        data={
            'title': 'Test workout',
        },
    )
    assert response.status_code == 201
