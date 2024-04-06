from django import forms

from app.core import fields as ff

from rich import print  # noqa


def test_StrictCharField_to_python_to_strip_whitespace_from_string():
    field = ff.StrictCharField()
    assert field.to_python('  test  ') == 'test'


def test_StrictCharField_to_python_to_return_none_if_value_is_none():
    field = ff.StrictCharField()
    assert field.to_python(None) is None


def test_StrictCharField_to_python_to_raise_error_if_value_is_not_string():
    field = ff.StrictCharField()
    try:
        field.to_python(123)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_StrictCharField_clean_to_raise_error_if_value_is_not_string():
    field = ff.StrictCharField()
    try:
        field.clean(123)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_StrictCharField_clean_to_return_cleaned_data():
    field = ff.StrictCharField()
    assert field.clean('  test  ') == 'test'


def test_StrictCharField_with_required_to_return_cleaned_data():
    field = ff.StrictCharField(required=True)
    assert field.clean('  test  ') == 'test'


def test_StrictCharField_with_required_to_raise_error_if_value_is_empty_string():
    field = ff.StrictCharField(required=True)
    try:
        field.clean('   ')
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_NestedFormField_to_python_to_return_data():
    class MockForm(forms.Form):
        field1 = forms.CharField()

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': 'test'}

    assert field.to_python(data) == data


def test_NestedFormField_clean_to_raise_error_if_form_is_invalid():
    class MockForm(forms.Form):
        field1 = ff.StrictCharField()

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': 123}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_NestedFormField_clean_to_return_cleaned_data():
    class MockForm(forms.Form):
        field1 = ff.StrictCharField()

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': 'test'}

    assert field.clean(data) == data


def test_NestedFormField_clean_with_required_with_a_empty_dict_to_raise_error():
    class MockForm(forms.Form):
        field1 = ff.StrictCharField()

    field = ff.NestedFormField(form_class=MockForm, required=True)
    data = {}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_NestedFormField_clean_with_required_children_field_to_raise_error_if_data_is_empty_dict():
    class MockForm(forms.Form):
        field1 = ff.StrictCharField(required=True)

    field = ff.NestedFormField(form_class=MockForm)
    data = {}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_NestedFormField_clean_with_required_children_field_to_raise_error_if_data_is_invalid():
    class MockForm(forms.Form):
        field1 = ff.StrictCharField(required=True)

    field = ff.NestedFormField(form_class=MockForm)
    data = {'field1': '   '}

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_ListField_to_python_to_return_data_if_it_is_a_list():
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


def test_ListField_clean_with_required_children_field_to_raise_error_if_data_is_empty_list():
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
    class MockForm(forms.Form):
        field1 = ff.StrictCharField()

    field = ff.ListField(children_field=ff.NestedFormField(form_class=MockForm))
    data = [{'field1': '1'}, {'field1': '2'}, {'field1': '3'}]

    assert field.clean(data) == data


def test_ListField_with_NestedFormField_children_field_to_raise_error_if_data_is_invalid():
    class MockForm(forms.Form):
        field1 = ff.StrictCharField()

    field = ff.ListField(children_field=ff.NestedFormField(form_class=MockForm))
    data = [{'field1': '1'}, {'field1': '2'}, {'field1': '  '}]

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)


def test_ListField_with_NestedFormField_children_field_to_raise_error_if_data_is_empty_list():
    class MockForm(forms.Form):
        field1 = ff.StrictCharField()

    field = ff.ListField(
        children_field=ff.NestedFormField(form_class=MockForm), required=True
    )
    data = []

    try:
        field.clean(data)
    except forms.ValidationError as e:
        assert isinstance(e, forms.ValidationError)
