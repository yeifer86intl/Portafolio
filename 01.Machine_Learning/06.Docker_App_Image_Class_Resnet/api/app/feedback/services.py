from app.auth.schema import TokenData
from app.user.models import User
from sqlalchemy.orm import Session

from . import models, schema


async def new_feedback(
    request: schema.Feedback, current_user: TokenData, database: Session
) -> models.Feedback:
    """
    Adds new feedback to the database associated with the current user.

    This asynchronous function creates a new feedback entry in the database using
    the provided feedback data and associates it with the current user. It first
    retrieves the user from the database based on the email in the `current_user` object,
    then creates and stores the new feedback entry.

    Args:
        request (schema.Feedback): An object containing the feedback details such as score,
                                   image file name, predicted class, and feedback text.
        current_user (TokenData): An object containing the email of the currently authenticated user.
        database (Session): The database session used for querying and committing changes to the database.

    Returns:
        models.Feedback: The newly created feedback entry stored in the database.

    Raises:
        Exception: If there is an issue with adding or committing the feedback to the database.
    """
    user = database.query(User).filter(User.email == current_user.email).first()
    new_feedback = models.Feedback(
        score=request.score,
        image_file_name=request.image_file_name,
        predicted_class=request.predicted_class,
        user=user,
        feedback=request.feedback,
    )
    database.add(new_feedback)
    database.commit()
    database.refresh(new_feedback)
    return new_feedback


async def all_feedback(database: Session, current_user: TokenData) -> models.Feedback:
    """
    Retrieves all feedback entries associated with the current user from the database.

    This asynchronous function queries the database for all feedback entries linked to
    the user identified by the `current_user` object. It returns a list of feedback entries
    associated with the user's ID.

    Args:
        database (Session): The database session used for querying the database.
        current_user (TokenData): An object containing the email of the currently authenticated user.

    Returns:
        list[models.Feedback]: A list of feedback entries associated with the current user.

    Raises:
        Exception: If there is an issue with querying the feedback entries from the database.
    """
    user = database.query(User).filter(User.email == current_user.email).first()
    return (
        database.query(models.Feedback).filter(models.Feedback.user_id == user.id).all()
    )
