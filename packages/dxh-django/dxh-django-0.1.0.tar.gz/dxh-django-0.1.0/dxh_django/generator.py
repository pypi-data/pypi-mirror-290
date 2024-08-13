import secrets
import string


def generate_verify_token(length=64, use_symbols=False):
    """
    Generate a secure, random verification token.

    Parameters:
    length (int): The length of the token. Default is 64.
    use_symbols (bool): Whether to include symbols in the token. Default is False.

    Returns:
    str: A randomly generated token consisting of ASCII letters, digits, and optionally symbols.
    """
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation
    token = ''.join(secrets.choice(characters) for _ in range(length))

    return token


def generate_sequential_code(prefix="", last_code=None, zfill_number=None):
    """
    Generate a new sequential code.

    Parameters:
    prefix (str): The prefix for the code.
    last_code (int): The last code number to increment. Default is 0.
    zfill_number (int): The number of digits to pad the code with leading zeros. Default is 0.

    Returns:
    str: The generated code.

    Example: generate_sequential_code("INV", 100, 5) -> "INV00101"
    """

    if last_code is not None:
        next_number = str(last_code + 1)
    else:
        next_number = str(1)

    if zfill_number is not None:
        next_number = next_number.zfill(zfill_number)

    return f"{prefix}{next_number}"
