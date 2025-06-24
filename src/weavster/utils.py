import re


def to_snake_case(string: str) -> str:
    """
    Convert a camelCase or PascalCase string to snake_case.
    """
    return re.sub(r"(?!^)(?=[A-Z])", "_", string).lower()
