import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app import db, settings as config, utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from sqlalchemy.orm import Session

router = APIRouter(tags=["Model"], prefix="/model")

@router.post("/predict", response_model=PredictResponse)
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    rpse = {"success": False, "prediction": None, "score": None, "image_file_name": None}

    # Verificar si se envió un archivo
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
    
    # Verificar si el archivo es una imagen válida
    if not utils.allowed_file(file.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type is not supported.")

    # Calcular el hash del archivo
    file_hash = await utils.get_file_hash(file)

    # Definir la ruta para guardar el archivo
    file_path = os.path.join(config.UPLOAD_FOLDER, str(file_hash))

    # Verificar si el archivo ya existe (basado en el hash)
    if not os.path.exists(file_path):
        # Guardar el archivo en disco
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

    # Enviar el archivo para procesarlo mediante el servicio de predicción del modelo
    prediction, score = await model_predict(file_hash)

    # Actualizar el diccionario de respuesta
    rpse["success"] = True
    rpse["prediction"] = prediction
    rpse["score"] = score
    rpse["image_file_name"] = file_hash

    return PredictResponse(**rpse)

"""
import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app import db, settings as config, utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from sqlalchemy.orm import Session

router = APIRouter(tags=["Model"], prefix="/model")

@router.post("/predict")
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    rpse = {"success": False, "prediction": None, "score": None, "image_file_name": None}
    
    # Verificar si se envió un archivo
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
    
    # Verificar si el archivo es una imagen
    if not utils.allowed_file(file.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
    
    # Calcular el hash del archivo
    file_hash = await utils.get_file_hash(file)
    
    #*********************************************************************************************
    # Definir la ruta para guardar el archivo
    file_path = os.path.join(config.UPLOAD_FOLDER, str(file_hash))
    
    # Verificar si el archivo ya existe (basado en el hash)
    if not os.path.exists(file_path):
        # Guardar el archivo en disco
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
    
    # Enviar el archivo para procesarlo mediante el servicio de predicción del modelo
    prediction, score = await model_predict(file_hash)
    
    # Actualizar el diccionario de respuesta
    rpse["success"] = True
    rpse["prediction"] = prediction
    rpse["score"] = score
    rpse["image_file_name"] = file_hash
    
    return PredictResponse(**rpse)
"""