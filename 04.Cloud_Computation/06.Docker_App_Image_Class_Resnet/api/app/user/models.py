from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import hashing


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    feedbacks = relationship("Feedback", back_populates="user")

    def __init__(self, name, email, password, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = hashing.get_password_hash(password)

    def check_password(self, password):
        return hashing.verify_password(self.password, password)
