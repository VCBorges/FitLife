from typing import Any

from apps.core import typed


def set_model_fields(model: typed.ModelType, fields: dict[str, Any]) -> None:
    for key, value in fields.items():
        setattr(model, key, value)


def default_translation(*fields) -> dict[str, dict[str, str]]:
    return {
        'en': {field: '' for field in fields},
        'pt': {field: '' for field in fields},
    }
