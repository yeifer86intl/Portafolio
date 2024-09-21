from pydantic import BaseModel


class PredictRequest(BaseModel):
    file: str


class PredictResponse(BaseModel):
    success: bool
    prediction: str
    score: float
    image_file_name: str
