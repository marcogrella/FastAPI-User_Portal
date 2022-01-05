from pydantic import BaseModel, EmailStr, ValidationError, validator
from datetime import datetime



class UserRequest(BaseModel):
    firstname: str
    lastname: str
    address: str
    cpf: str
    email: EmailStr
    senha: str
    contrasenha: str

