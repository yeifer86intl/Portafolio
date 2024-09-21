from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schema


async def new_user_register(request: schema.User, database: Session) -> models.User:
    """
    Registers a new user in the database.

    This asynchronous function creates a new user entry in the database using the provided
    user details from the request. It adds the user to the database, commits the changes,
    and returns the newly created user.

    Args:
        request (schema.User): An object containing user details such as name, email, and password.
        database (Session): The database session used for adding and committing the user to the database.

    Returns:
        models.User: The newly created user entry stored in the database.
    """
    new_user = models.User(
        name=request.name, email=request.email, password=request.password
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


async def all_users(database: Session) -> models.User:
    """
    Retrieves all users from the database.

    This asynchronous function queries the database to retrieve a list of all users.

    Args:
        database (Session): The database session used for querying the database.

    Returns:
        list[models.User]: A list of all user entries in the database.
    """
    return database.query(models.User).all()


async def get_user_by_id(id: int, database: Session) -> models.User:
    """
    Retrieves a user from the database by their ID.

    This asynchronous function queries the database for a user with the specified ID.
    If the user is not found, an HTTP 404 Not Found exception is raised.

    Args:
        id (int): The ID of the user to retrieve.
        database (Session): The database session used for querying the database.

    Returns:
        models.User: The user entry with the specified ID.

    Raises:
        HTTPException: If the user with the specified ID is not found.
    """
    user = database.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user


async def delete_user_by_id(id: int, database: Session):
    """
    Deletes a user from the database by their ID.

    This asynchronous function removes the user with the specified ID from the database
    and commits the changes.

    Args:
        id (int): The ID of the user to delete.
        database (Session): The database session used for querying and committing changes to the database.
    """
    database.query(models.User).filter(models.User.id == id).delete()
    database.commit()
