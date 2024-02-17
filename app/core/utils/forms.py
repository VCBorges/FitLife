from typing import TypeVar

from django.forms import Form

T = TypeVar('T', bound=Form)


def get_form_errors(form: T) -> dict[str, list[str]]:
    return {'errors': form.errors}
