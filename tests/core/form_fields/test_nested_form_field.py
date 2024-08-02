from django import forms

from src.core import form_fields
from src.core.forms import BaseForm

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

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_to_return_cleaned_data():
    class MockForm(BaseForm):
        field1 = form_fields.StrictCharField()

    field = form_fields.NestedFormField(form_class=MockForm)
    data = {'field1': 'test'}

    assert field.clean(data) == data


def test_clean_with_required_when_receive_a_empty_dict_to_raise_error():
    class MockForm(BaseForm):
        field1 = form_fields.StrictCharField()

    field = form_fields.NestedFormField(form_class=MockForm, required=True)
    data = {}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_with_required_children_field_to_raise_error_if_data_is_empty_dict():
    class MockForm(BaseForm):
        field1 = form_fields.StrictCharField(required=True)

    field = form_fields.NestedFormField(form_class=MockForm)
    data = {}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_with_required_children_field_to_raise_error_if_data_is_invalid():
    class ChildForm(BaseForm):
        field1 = form_fields.StrictCharField(required=True)

    field = form_fields.NestedFormField(form_class=ChildForm)
    data = {'field1': '   '}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_somethigng():
    class ChildForm(BaseForm):
        child_field1 = form_fields.StrictCharField(required=True)

    class ParentForm(BaseForm):
        nested_field = form_fields.NestedFormField(form_class=ChildForm)

    form = ParentForm(data={'nested_field': {'child_field1': 1}})

    print(f'{form.is_valid() = }')
    # print(f'{form.errors = }')
    # print(f'{form.errors["nested_field"] = }')
    # print(f'{type(form.errors["nested_field"]) = }')
    # assert False
