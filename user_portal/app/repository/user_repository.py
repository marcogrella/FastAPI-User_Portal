from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app import models, database, schemas
from fastapi import HTTPException, Response, status
from app import utils


def create_user(usuario_dto: schemas.UserRequest, db: Session):
    
    usuario_cpf = consulta_usuario_cpf(usuario_dto.cpf, db)

    if usuario_cpf:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"CPF já cadastrado para outro usuário")
    
    usuario_email = consulta_usuario_email(usuario_dto.email, db)
    if usuario_email:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"O email '{usuario_email.email}' já está em uso" )
    
    senha_criptografada = utils.hash(usuario_dto.senha)
    usuario_dto.senha = senha_criptografada
    novo_usuario = models.Usuario(**usuario_dto.dict())
    
    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)        
    except:        
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Um erro interno ocorreu, entre em contato com o administrador.")

    return novo_usuario


def delete_user(id: int, db: Session):
    usuario_consulta = consultar_usuario_por_id(id, db)
    try:
        usuario_consulta.delete(synchronize_session=False)
        db.commit()    
    except:        
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Um erro interno ocorreu, entre em contato com o administrador.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update_user(id: int, usuario_dto: schemas.UserRequestUpdate, db: Session):
    usuario_atual = consultar_usuario_por_id(id, db)

    # consulta para verificar se o cpf está em uso  
    usuario_cpf = consulta_usuario_cpf(usuario_dto.cpf, db)

    # se o cpf estiver em uso e for do mesmo usuário, então pode ser atualizado. Caso contrário (o cpf da requisição pertencer a outro usuário) a exceção é levantada
    if usuario_cpf:
        if usuario_atual.first().cpf != usuario_dto.cpf:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"CPF já cadastrado para outro usuário")

    # consulta para verificar se o cpf está em uso  
    usuario_email = consulta_usuario_email(usuario_dto.email, db)
    
    # se o email estiver em uso e for do mesmo usuário, então pode ser atualizado. Caso contrário (o email da requisição pertencer a outro usuário) a exceção é levantada
    if usuario_email:
        if usuario_atual.first().email != usuario_dto.email:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"{usuario_dto.email} já cadastrado para outro usuário")


    try:
        usuario_atual.update(usuario_dto.dict(), synchronize_session=False)
        db.commit()
        return usuario_atual.first()
    
    except:        
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Um erro interno ocorreu, entre em contato com o administrador.")
    

def consultar_usuario_por_id(id: int, db: Session):
    usuario_consulta = db.query(models.Usuario).filter(models.Usuario.id == id)
    if not usuario_consulta.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Usuário com id '{id}' não está disponível")
    return usuario_consulta


def consulta_avancada(db: Session, limit: int, skip: int, search: Optional[str] = ""):
    if search != "":
        usuarios = db.query(models.Usuario).filter(models.Usuario.nome.contains(search)).limit(limit).offset(skip).all()
        return usuarios

    usuarios = db.query(models.Usuario).limit(limit).offset(skip).all()
    return usuarios


def consulta_usuario_cpf(cpf: str, db: Session):
    return db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
 

def consulta_usuario_email(email: str, db: Session):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()
    



