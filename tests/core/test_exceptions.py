from apps.core import exceptions


def test_BaseError_error_dict_to_be_the_same_as_data():
    # Arrange
    data = {'error': 'An error occurred'}

    # Act
    error = exceptions.BaseError(
        message='An error occurred',
        status_code=400,
        data=data,
    )

    # Assert
    assert error.error_dict == data


def test_BaseError_message_to_be_the_same_as_message():
    # Arrange
    message = 'An error occurred'

    # Act
    error = exceptions.BaseError(
        message=message,
        status_code=400,
        data={'error': 'An error occurred'},
    )

    # Assert
    assert error.message == message


def test_BaseError_status_code_to_be_the_same_as_status_code():
    # Arrange
    status_code = 400

    # Act
    error = exceptions.BaseError(
        message='An error occurred',
        status_code=status_code,
        data={'error': 'An error occurred'},
    )

    # Assert
    assert error.status_code == status_code


def test_FormValidationError_error_dict_to_be_the_same_as_errors():
    # Arrange
    errors = {'error': 'An error occurred'}

    # Act
    error = exceptions.FormValidationError(
        errors=errors,
    )

    # Assert
    assert error.error_dict == errors


def test_FormValidationError_default_status_code_to_be_400():
    # Act
    error = exceptions.FormValidationError(
        errors={'error': 'An error occurred'},
    )

    # Assert
    assert error.status_code == 400


def test_FormValidationError_default_message_to_be_Invalid_data():
    # Act
    error = exceptions.FormValidationError(
        errors={'error': 'An error occurred'},
    )

    # Assert
    assert error.message == 'Invalid data.'


def test_FieldValidationError_error_dict_to_be_the_same_as_data():
    # Arrange
    data = {
        'string_field': 'test',
        'list_field': [
            {
                'int_field': 1,
                'float_field': 1.0,
            },
            {
                'int_field': 2,
            },
        ],
        'dict_field': {
            'int_field': 1,
            'float_field': 1.0,
        },
    }

    # Act
    error = exceptions.FieldValidationError(data=data)

    # Assert
    assert error.error_dict == data
