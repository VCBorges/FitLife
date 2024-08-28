from django import forms

from apps.core import form_fields as ff

from rich import print  # noqa


def test_to_python_to_strip_whitespace_from_string():
    field = ff.StrictCharField()
    assert field.to_python('  test  ') == 'test'


def test_to_python_to_return_none_if_value_is_none():
    field = ff.StrictCharField()
    assert field.to_python(None) is None


def test_to_python_to_raise_error_if_value_is_not_string():
    field = ff.StrictCharField()
    try:
        field.to_python(123)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_to_raise_error_if_value_is_not_string():
    field = ff.StrictCharField()
    try:
        field.clean(123)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_clean_to_return_cleaned_data():
    field = ff.StrictCharField()
    assert field.clean('  test  ') == 'test'


def test_with_required_to_return_cleaned_data():
    field = ff.StrictCharField(required=True)
    assert field.clean('  test  ') == 'test'


def test_with_required_to_raise_error_if_value_is_empty_string():
    field = ff.StrictCharField(required=True)
    try:
        field.clean('   ')
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)
