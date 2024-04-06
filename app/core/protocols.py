from django.http import HttpRequest

from app.users.models import Users


class AuthenticatedRequest(HttpRequest):
    """
    A protocol like class for type hinting authenticated requests in Django, combining HttpRequest
    and custom authenticated user attributes.

    Inherits:
        HttpRequest: Inherits from Django's HttpRequest to include all standard request properties and methods.
        Protocol: Allows for runtime structural type checking.

    Attributes:
        user: Users model, representing the authenticated user associated with the request.
    """

    user: Users
