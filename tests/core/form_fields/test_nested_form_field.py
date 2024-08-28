from django import forms
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.core import form_fields
from apps.core.forms import BaseForm

import pytest
from rich import print  # noqa


def test_to_python_to_return_a_python_dict():
    class MockForm(BaseForm):
        field1 = forms.CharField()

    field = form_fields.NestedFormField(form_class=MockForm)
    data = {'field1': 'test'}

    assert field.to_python(data) == data


def test_clean_to_raise_error_when_child_form_is_invalid():
    class MockForm(BaseForm):
        field1 = form_fields.StrictCharField()

    field = form_fields.NestedFormField(form_class=MockForm)
    data = {'field1': 123}

    with pytest.raises(DjangoValidationError):
        field.clean(data)


def test_clean_to_return_cleaned_data():
    class MockForm(BaseForm):
        field1 = form_fields.StrictCharField()

    field = form_fields.NestedFormField(form_class=MockForm)
    data = {'field1': 'test'}

    # with pytest
    assert field.clean(data) == data


def test_clean_with_required_when_receive_a_empty_dict_to_raise_error():
    class MockForm(BaseForm):
        field1 = form_fields.StrictCharField()

    field = form_fields.NestedFormField(form_class=MockForm, required=True)
    data = {}

    with pytest.raises(DjangoValidationError):
        field.clean(data)


def test_clean_with_required_children_field_to_raise_error_if_data_is_empty_dict():
    class MockForm(BaseForm):
        field1 = form_fields.StrictCharField(required=True)

    field = form_fields.NestedFormField(form_class=MockForm)
    data = {}

    with pytest.raises(DjangoValidationError):
        field.clean(data)


def test_clean_with_required_children_field_to_raise_error_if_data_is_invalid():
    class ChildForm(BaseForm):
        field1 = form_fields.StrictCharField(required=True)

    field = form_fields.NestedFormField(form_class=ChildForm)
    data = {'field1': '   '}

    with pytest.raises(DjangoValidationError):
        field.clean(data)


def test_is_valid_in_a_parent_form_to_errors_have_child_field1():
    class ChildForm(BaseForm):
        child_field1 = form_fields.StrictCharField(required=True)
        child_field2 = form_fields.StrictCharField(required=True)

    class ParentForm(BaseForm):
        nested_field = form_fields.NestedFormField(form_class=ChildForm)

    form = ParentForm(data={'nested_field': {'child_field1': 1}})

    form.is_valid(raise_exception=False)

    assert 'child_field1' in form.errors['nested_field']


def test_is_valid_with_child_nested_form_field_have_correct_keys():
    class ChildChildForm(BaseForm):
        child_child_field1 = form_fields.StrictCharField(required=True)

    class ChildForm(BaseForm):
        child_field1 = form_fields.NestedFormField(
            form_class=ChildChildForm, required=True
        )

    class ParentForm(BaseForm):
        nested_field = form_fields.NestedFormField(form_class=ChildForm, required=True)

    form = ParentForm(
        data={'nested_field': {'child_field1': {'child_child_field1': ''}}}
    )

    form.is_valid(raise_exception=False)

    assert 'child_child_field1' in form.errors['nested_field']['child_field1']
