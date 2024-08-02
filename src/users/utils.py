from django.contrib.auth import get_user_model as django_get_user_model

from src.users.models import Users

UserModel = type[Users]


def get_user_model() -> type[Users]:
    return django_get_user_model()
