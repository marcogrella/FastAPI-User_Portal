from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.engine.interfaces import ExceptionContext
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app import schemas, utils, models
from app.database import get_db
from repository import user_repository
from typing import List, Optional




router = APIRouter(
    prefix="/users",  # cria o prefixo automaticamente em cada endpoint
    tags=['Users'] # cria um grupo para a documentação. http://127.0.0.1:8000/docs
)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_dto: schemas.UserRequest, db: Session = Depends(get_db)):
    return user_repository.create_user(user_dto, db)
    


@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_repository.delete_user(id, db)  


@router.put('/{id}', status_code = status.HTTP_200_OK, response_model=schemas.UserResponse)
def update_user(id: int, user_dto: schemas.UserRequestUpdate, db: Session = Depends(get_db)):
    return user_repository.update_user(id, user_dto, db)


# for test: http://127.0.0.1:8000/users/?skip=0&limit=10&search=test

@router.get("/", response_model=List[schemas.UserResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return user_repository.consulta_avancada(db, limit, skip, search)



@router.get('/{id}', status_code = status.HTTP_200_OK, response_model=schemas.UserResponse)
def update_user(id: int, db: Session = Depends(get_db)):
    return user_repository.consultar_usuario_por_id(id, db).first()

