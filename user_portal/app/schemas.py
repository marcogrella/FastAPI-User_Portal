from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    nome: str
    sobrenome: str
    endereco: str
    cpf: str
    email: EmailStr
    senha: str


class UserRequestUpdate(BaseModel):
    nome: str
    sobrenome: str
    endereco: str
    cpf: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    endereco: str
    cpf: str
    email: EmailStr
    data_criacao: datetime
    


    class Config:      
         orm_mode = True