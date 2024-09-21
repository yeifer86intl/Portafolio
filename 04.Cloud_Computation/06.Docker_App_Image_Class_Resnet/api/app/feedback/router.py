from typing import List

from app import db
from app.auth.jwt import get_current_user
from app.user.schema import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import schema, services

router = APIRouter(tags=["Feedback"], prefix="/feedback")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_feedback(
    request: schema.Feedback,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.new_feedback(request, current_user, database)


@router.get("/", response_model=List[schema.DisplayFeedback])
async def get_all_feedback(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.all_feedback(database, current_user)

#Este código define un router para gestionar feedback en una API. Contiene dos rutas:

#POST para crear un feedback.
#GET para obtener todos los feedbacks.
#Utiliza FastAPI para gestionar dependencias y autenticación con JWT, y SQLAlchemy para interactuar con la base de datos. 
# La lógica de negocio está delegada a los módulos services, manteniendo el controlador limpio y enfocado en manejar las solicitudes y
# respuestas.