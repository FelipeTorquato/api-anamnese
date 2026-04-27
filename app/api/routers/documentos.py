from typing import Optional, List

from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.params import Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models import TipoDocumento, Usuario
from app.schemas.documento import DocumentoResponse
from app.services import documento_service

router = APIRouter(prefix="/pacientes", tags=["Documentos e Laudos"], dependencies=[Depends(get_current_user)])


@router.post("/{paciente_id}/documentos", response_model=DocumentoResponse, status_code=status.HTTP_201_CREATED)
def anexar_documento(paciente_id: int, arquivo: UploadFile = File(..., description="Arquivo PDF ou imagem"),
                     tipo: TipoDocumento = Form(..., description="LAUDO_MEDICO, RECEITA_MEDICA etc."),
                     observacao: Optional[str] = Form(None, description="Anotaçãoes adicionais"),
                     db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return documento_service.anexar_documento(db, paciente_id, arquivo, tipo, observacao, current_user)


@router.get("/{paciente_id}/documentos", response_model=List[DocumentoResponse])
def listar_documentos(paciente_id: int, db: Session = Depends(get_db)):
    return documento_service.listar_documentos_paciente(db, paciente_id)


@router.get("/{paciente_id}/documentos/{documento_id}/download", summary="Download de Laudos/Anexos")
def baixar_documento(paciente_id: int, documento_id: int, db: Session = Depends(get_db),
                     current_user: Usuario = Depends(get_current_user)):
    caminho_arquivo = documento_service.obter_caminho_download(db, paciente_id=paciente_id, documento_id=documento_id)

    nome_arquivo = caminho_arquivo.split("/")[-1]

    return FileResponse(path=caminho_arquivo, filename=nome_arquivo, media_type="application/octet-stream")
