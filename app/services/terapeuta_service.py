from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Terapeuta
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.terapeuta import TerapeutaCreate
from app.models import TipoUsuario
from app.repositories.terapeuta_repository import TerapeutaRepository


def criar_terapeuta(db: Session, terapeuta_in: TerapeutaCreate) -> Terapeuta:
    usuario = UsuarioRepository.buscar_por_id(db, terapeuta_in.usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if usuario.perfil != TipoUsuario.TERAPEUTA:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="O usuário informado não possui o perfil de Terapeuta")

    existente = TerapeutaRepository.buscar_por_usuario_id(db, terapeuta_in.usuario_id)
    if existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Este usuároi já está vinculado a um perfil de Terapeuta")

    novo_terapeuta = Terapeuta(**terapeuta_in.model_dump())
    return TerapeutaRepository.criar(db, novo_terapeuta)


def listar_terapeutas(db: Session, skip: int = 0, limit: int = 100) -> List[Terapeuta]:
    return TerapeutaRepository.listar(db, skip, limit)


def buscar_terapeuta(db: Session, terapeuta_id: int) -> Terapeuta:
    terapeuta = TerapeutaRepository.buscar_por_id(db, terapeuta_id)
    if not terapeuta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Terapeuta não encontrado")
    return terapeuta
