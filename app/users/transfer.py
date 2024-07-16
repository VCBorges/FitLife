from dataclasses import dataclass

from app.core.transfer import BaseDTO


@dataclass
class CreateUserDTO(BaseDTO):
    email: str
    password: str
    first_name: str
    last_name: str
    birth_date: str
    document: str


@dataclass
class UpdateUserDTO(BaseDTO):
    email: str
    first_name: str
    last_name: str
    birth_date: str
    document: str
