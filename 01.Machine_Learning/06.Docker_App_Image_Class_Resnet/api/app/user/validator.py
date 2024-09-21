from typing import Optional

from sqlalchemy.orm import Session

from .models import User


async def verify_email_exist(email: str, database: Session) -> Optional[User]:
    """
    Checks if a user with the specified email exists in the database.

    This asynchronous function queries the database to find a user with the given email.
    It returns the user object if found, or `None` if no user with that email exists.

    Args:
        email (str): The email address to check for existence.
        database (Session): The database session used for querying the database.

    Returns:
        Optional[User]: The user object if a user with the specified email exists, otherwise `None`.
    """
    return database.query(User).filter(User.email == email).first()
