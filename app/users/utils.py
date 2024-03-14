def clean_cpf(cpf: str) -> str:
    return ''.join(char for char in cpf if char.isdigit())
