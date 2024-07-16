from django.forms.utils import ErrorDict

from app.core.types import FormType


def get_form_errors(form: FormType) -> ErrorDict:
    return {'errors': form.errors}


def are_all_fields_in_cleaned_data(
    form: FormType,
    fields: list[str] = None,
) -> bool:
    if fields is None:
        fields = form.fields.keys()
    return all(field in form.cleaned_data for field in fields)
