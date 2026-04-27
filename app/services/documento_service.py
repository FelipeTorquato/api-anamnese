import os
import shutil
import uuid

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models import Documento
from app.models import TipoDocumento
from app.models import Usuario
from app.repositories.documento_repository import DocumentoRepository
from app.repositories.paciente_repository import PacienteRepository

UPLOAD_DIR = "uploads/documentos"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def anexar_documento(db: Session, paciente_id: int, arquivo: UploadFile, tipo: TipoDocumento, observacao: str,
                     current_user: Usuario) -> Documento:
    paciente = PacienteRepository.buscar_por_id(db, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    extensao = arquivo.filename.split(".")[-1].lower()
    extensoes_permitidas = ["pdf", "jpg", "jpeg", "png"]
    if extensao not in extensoes_permitidas:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Formato de arquivo não permitido. Use: {', '.join(extensoes_permitidas)}")

    nome_seguro = f"{uuid.uuid4()}.{extensao}"
    caminho_completo = os.path.join(UPLOAD_DIR, nome_seguro)

    try:
        with open(caminho_completo, 'wb') as buffer:
            shutil.copyfileobj(arquivo.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ocorreu um erro ao salvar o arquivo no servidor")
    finally:
        arquivo.file.close()

    novo_documento = Documento(paciente_id=paciente_id, tipo=tipo, observacao=observacao, caminho_arquivo=nome_seguro,
                               created_by=current_user.email)

    return DocumentoRepository.criar(db, novo_documento)


def listar_documentos_paciente(db: Session, paciente_id: int) -> list[Documento]:
    return DocumentoRepository.listar_por_paciente(db, paciente_id)
