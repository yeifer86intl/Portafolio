from app.db import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float)
    predicted_class = Column(String(50))
    feedback = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    image_file_name = Column(String(255))
    user = relationship("User", back_populates="feedbacks")

    def __init__(
        self, score, predicted_class, feedback, image_file_name, user, *args, **kwargs
    ):
        self.predicted_class = predicted_class
        self.feedback = feedback
        self.score = score
        self.image_file_name = image_file_name
        self.user = user
