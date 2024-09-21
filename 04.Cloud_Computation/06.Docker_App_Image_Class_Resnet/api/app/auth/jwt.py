from datetime import datetime, timedelta

from app.settings import SECRET_KEY
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schema

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """
    Generates a JWT access token with an expiration time.

    This function creates a JWT (JSON Web Token) that includes the provided
    data and an expiration time. The token is signed using a secret key and
    a specified algorithm.

    Args:
        data (dict): A dictionary containing the data to be included in the token.

    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verifies the provided JWT token and extracts the user information.

    This function decodes the given JWT token using the secret key and specified
    algorithm. It checks for the presence of the user's email in the token's payload.
    If the email is not found or the token is invalid, an exception is raised.

    Args:
        token (str): The JWT token to be verified.
        credentials_exception: The exception to raise if the token is invalid or the email is not found.

    Returns:
        TokenData: An object containing the user's email extracted from the token.

    Raises:
        credentials_exception: If the token is invalid or does not contain an email.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current authenticated user based on the provided JWT token.

    This function extracts the JWT token from the request, verifies it, and returns
    the user data associated with the token. If the token is invalid or cannot be
    verified, an HTTP 401 Unauthorized exception is raised.

    Args:
        token (str, optional): The JWT token extracted from the request using the OAuth2
                               password flow. Defaults to being fetched via `Depends(oauth2_scheme)`.

    Returns:
        TokenData: An object containing the user's information extracted from the token.

    Raises:
        HTTPException: If the token is invalid or the credentials cannot be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
