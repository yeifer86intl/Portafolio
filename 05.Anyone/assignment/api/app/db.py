from app import settings as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.DATABASE_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Provides a database session for dependency injection.

    This function is used to obtain a new database session instance from the
    `SessionLocal` factory. It is intended to be used with dependency injection
    in FastAPI to manage database sessions.

    Yields:
        Session: A SQLAlchemy database session.

    Notes:
        The session is automatically closed after use to ensure proper resource management.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
