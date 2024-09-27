from __future__ import annotations

import typing as tp

from django.db.models import Model
from django.forms import Field
from django.http import HttpRequest

from apps.core.forms import BaseForm

if tp.TYPE_CHECKING:
    from apps.users.models import Users

DjangoModelType = tp.TypeVar('DjangoModelType', bound=Model)
BaseFormType = tp.TypeVar('BaseFormType', bound=BaseForm)
FieldType = tp.TypeVar('FieldType', bound=Field)


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
