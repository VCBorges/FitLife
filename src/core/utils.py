from typing import Any

from src.core import typed


def set_model_fields(model: typed.ModelType, fields: dict[str, Any]) -> None:
    for key, value in fields.items():
        setattr(model, key, value)
