from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verifies if the provided plain password matches the hashed password.

    This function compares a plain password with a hashed password to check if they
    match using the Argon2 hashing algorithm. It returns `True` if the passwords match,
    otherwise returns `False`.

    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: `True` if the plain password matches the hashed password, otherwise `False`.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hashes the provided password using the Argon2 algorithm.

    This function generates a hashed version of the given plain text password using
    the Argon2 hashing algorithm. The resulting hash can be used for secure password storage.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)
