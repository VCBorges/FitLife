from django.core.exceptions import ValidationError

from apps.core.constants import Language


def translated_field_validator(value: dict[str, str]) -> None:
    """
    Validates that the translated field contains both 'en' and 'pt' keys.

    Parameters
    ----------
        - value (dict[str, str]): A dictionary containing language codes as keys
            and translated strings as values.

    Raises
    ------
        ValidationError: If either 'en' or 'pt' key is missing.
    """
    required_languages = {
        Language.EN,
        Language.PT,
    }
    provided_languages = set(value.keys())

    missing_languages = required_languages - provided_languages
    if missing_languages:
        raise ValidationError(
            f"Missing required language(s): {', '.join(missing_languages)}. "
            f"Both 'en' and 'pt' translations must be provided."
        )
