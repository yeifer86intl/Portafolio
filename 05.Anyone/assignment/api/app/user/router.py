from typing import List

from app import db
from app.auth.jwt import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import schema, services, validator

router = APIRouter(tags=["Users"], prefix="/user")

#-------------------------------------------------------------
#ORIGINAL
"""
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_registration(
    request: schema.User, database: Session = Depends(db.get_db)
):
    # TODO: Implement the create_user_registration endpoint
    # Make sure to:
    #  1. Verify the user email doesn't already exist, see `verify_email_exist()` function under `validator.py`
    #  2. If the email already exists, raise a 400 HTTPException
    #  3. If the email doesn't exist, create a new user, see `new_user_register()` function under `services.py`
    #  4. Return the new user object created

    new_user = None

    return new_user

#-------------------------------------------------------------
"""
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_registration(
    request: schema.User, database: Session = Depends(db.get_db)
):
    # 1. Verificar si el correo ya existe
    existing_user = await validator.verify_email_exist(request.email, database)
    
    # 2. Si el correo ya existe, lanzar una excepción HTTP 400
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 3. Registrar un nuevo usuario si el correo no existe
    new_user = await services.new_user_register(request, database)
    
    # 4. Devolver el objeto del nuevo usuario creado
    return new_user

#-------------------------------------------------------------

@router.get("/")
async def get_all_users(
    database: Session = Depends(db.get_db),
    current_user: schema.User = Depends(get_current_user),
):
    return await services.all_users(database)


@router.get("/{id}", response_model=schema.DisplayUser)
async def get_user_by_id(
    id: int,
    database: Session = Depends(db.get_db),
    current_user: schema.User = Depends(get_current_user),
):
    return await services.get_user_by_id(id, database)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    id: int,
    database: Session = Depends(db.get_db),
    current_user: schema.User = Depends(get_current_user),
):
    return await services.delete_user_by_id(id, database)
