from typing import TypeVar

from django.db.models import Model
from django.forms import Field
from django.http import HttpRequest

from apps.core.forms import BaseForm
from apps.users.models import Users

DjangoModelType = TypeVar('DjangoModelType', bound=Model)
BaseFormType = TypeVar('BaseFormType', bound=BaseForm)
FieldType = TypeVar('FieldType', bound=Field)


class AuthenticatedRequest(HttpRequest):
    """
    A protocol like class for type hinting authenticated requests in Django,
    combining HttpRequest and custom authenticated user attributes.

    Attributes:
    -----------
        user: Users model, representing the authenticated user associated with the
        request.
    """

    user: Users
