from pydantic import BaseModel


class Feedback(BaseModel):
    score: float
    predicted_class: str
    image_file_name: str
    feedback: str


class DisplayFeedback(BaseModel):
    id: int
    score: float
    predicted_class: str
    image_file_name: str
    feedback: str

    class Config:
        orm_mode = True
