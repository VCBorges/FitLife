from django import forms

from app.core import fields as ff
from app.core.forms import BaseForm

from rich import print  # noqa


def test_to_python_to_return_data():
    class MockForm(BaseForm):
        field1 = forms.CharField()

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': 'test'}

    assert field.to_python(data) == data


def test_clean_to_raise_error_if_form_is_invalid():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField()

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': 123}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_to_return_cleaned_data():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField()

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': 'test'}

    assert field.clean(data) == data


def test_clean_with_required_with_a_empty_dict_to_raise_error():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField()

    field = ff.NestedFormField(form_class=MockForm, required=True)
    data = {}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_with_required_children_field_to_raise_error_if_data_is_empty_dict():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField(required=True)

    field = ff.NestedFormField(form_class=MockForm)
    data = {}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_with_required_children_field_to_raise_error_if_data_is_invalid():
    class MockForm(BaseForm):
        field1 = ff.StrictCharField(required=True)

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': '   '}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


# def test_in():
#     data = {
#         'field1': {
#             'field2': 1,
#         }
#     }
#     class MockForm(BaseForm):
#         field2 = ff.StrictCharField(required=True)

#     class MockNestedForm(BaseForm):
#         field1 = ff.NestedFormField(form_class=MockForm, required=True)

#     form = MockNestedForm(data=data)
#     print(f'{form.is_valid() = }')
#     print(f'{form.errors = }')

#     assert False
