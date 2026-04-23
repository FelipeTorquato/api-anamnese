from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.models import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate


def criar_usuario(db: Session, usuario_in: UsuarioCreate) -> Usuario:
    if UsuarioRepository.buscar_por_email(db, usuario_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

    hashed_pw = security.get_password_hash(usuario_in.password)

    novo_usuario = Usuario(email=usuario_in.email, perfil=usuario_in.perfil, hashed_password=hashed_pw)

    return UsuarioRepository.criar(db, novo_usuario)
