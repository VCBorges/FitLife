from typing import Any


def remove_dict_none_values(data: dict[str, Any]) -> dict[str, Any]:
    """
    Removes all key-value pairs from the dictionary where the value is None.

    Parameters:
    - data (Dict[str, Any]): The dictionary from which to remove key-value pairs with None values.

    Returns:
    - dict[str, Any]: A new dictionary with None values removed.

    Example:
    >>> sample_dict = {'a': 1, 'b': None, 'c': 'test', 'd': None}
    >>> print(remove_none_values(sample_dict))
    {'a': 1, 'c': 'test'}
    """
    return {key: value for key, value in data.items() if value is not None}
