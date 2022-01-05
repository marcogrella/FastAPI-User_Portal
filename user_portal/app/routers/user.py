from fastapi import status, HTTPException, Depends, APIRouter
from app.dto import schemas
from app.exceptions import customexceptions
from app.utils import utils

router = APIRouter(
    prefix="/users",  # cria o prefixo automaticamente em cada endpoint
    tags=['Users'] # cria um grupo para a documentação. http://127.0.0.1:8000/docs
)


@router.post("/", status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserRequest):

    if user.senha != user.contrasenha:
        raise customexceptions.PasswordsNotMatchException(status_code = status.HTTP_400_BAD_REQUEST,
                                            detail= f"Atenção, senha e contrasenha não correspondem.")

    hashed_senha = utils.hash(user.senha)
    user.senha = hashed_senha
    print(hashed_senha)

    return {"user": user.firstname}