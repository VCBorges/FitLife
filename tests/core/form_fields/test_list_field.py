from django import forms

from apps.core import form_fields as ff
from apps.core.forms import BaseForm

from rich import print  # noqa


def test_to_python_to_return_data_if_it_is_a_list():
    field = ff.ListField(children_field=ff.StrictCharField())
    data = ['1', '2', '3']

    assert field.to_python(data) == data


def test_ListField_to_python_to_raise_error_if_data_is_not_a_list():
    field = ff.ListField(children_field=ff.StrictCharField())
    data = '1, 2, 3'

    try:
        field.to_python(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_ListField_clean_to_raise_error_if_data_is_not_a_list():
    field = ff.ListField(children_field=ff.StrictCharField())
    data = '1, 2, 3'

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_with_required_children_field_to_raise_error_if_data_is_empty_list():
    field = ff.ListField(children_field=ff.StrictCharField(), required=True)
    data = []

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_ListField_clean_to_return_cleaned_data():
    field = ff.ListField(children_field=ff.StrictCharField())
    data = ['1', '2', '3']

    assert field.clean(data) == data


def test_ListField_with_NestedFormField_children_field_to_return_cleaned_data():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField()

    field = ff.ListField(children_field=ff.NestedFormField(form_class=MockForm))
    data = [{'field1': '1'}, {'field1': '2'}, {'field1': '3'}]

    assert field.clean(data) == data


def test_ListField_with_NestedFormField_children_field_to_raise_error_if_data_is_invalid():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField()

    field = ff.ListField(children_field=ff.NestedFormField(form_class=MockForm))
    data = [{'field1': '1'}, {'field1': None}, {'field1': '  '}]

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_with_NestedFormField_children_field_to_raise_error_if_data_is_empty_list():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField()

    field = ff.ListField(
        children_field=ff.NestedFormField(form_class=MockForm), required=True
    )
    data = []

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)
