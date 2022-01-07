from sqlalchemy import String, Column, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    data_criacao = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))