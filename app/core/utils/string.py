import re


def has_special_characters(string: str) -> bool:
    """
    Checks if the given string has any special characters.

    Parameters:
    s (str): The string to check for special characters.

    Returns:
    bool: True if there are special characters, False otherwise.
    """
    # This regex pattern matches any character that is NOT a letter (a-z, A-Z) or a number (0-9).
    pattern = re.compile('[^a-zA-Z0-9]')
    return bool(pattern.search(string))
