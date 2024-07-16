from dataclasses import asdict, astuple, dataclass, fields
from typing import Any, Generic

from app.core.types import ModelType
from app.core.utils.common import remove_dict_none_values


@dataclass
class BaseDTO:
    def to_dict(self) -> dict[str, Any]:
        return remove_dict_none_values(asdict(self))

    def to_tuple(self):
        return tuple(filter(lambda x: x is not None), astuple(self))

    @classmethod
    def get_field_names(cls) -> tuple[str]:
        """Return a tuple with all the field names of the dataclass.

        Returns:
            tuple: A tuple containing all the field names.
        """
        return tuple(field.name for field in fields(cls))


@dataclass
class UpdateDTO(BaseDTO, Generic[ModelType]):
    instance: ModelType

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data['instance']
        return data

    @classmethod
    def get_field_names(cls) -> tuple[str]:
        """Return a tuple with all the field names of the dataclass.

        Returns:
            tuple: A tuple containing all the field names.
        """
        return tuple(field.name for field in fields(cls) if field.name != 'instance')
