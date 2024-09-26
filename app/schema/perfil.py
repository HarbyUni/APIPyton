from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.schema.base import BodySchema, ResponseSchema


class PerfilUsuarioSchema(BaseModel):
    id_perfil: str = Field(..., description="ID único del perfil de usuario")
    id: str = Field(..., description="ID del usuario asociado")
    nombre_usuario: str = Field(..., description="Nombre de usuario")
    foto: Optional[str] = Field(None, description="URL de la foto del usuario")
    codigo_qr: Optional[str] = Field(None, description="Código QR del usuario")
    mensaje_estado: Optional[str] = Field(None, description="Mensaje de estado del usuario")
    nivel_usuario: Optional[int] = Field(None, description="Nivel del usuario")
    total_puntos: Optional[int] = Field(None, description="Total de puntos acumulados")

    

class CreatePerfilUsuarioSchema(BaseModel):
    id: str = Field(..., description="ID del usuario asociado")
    nombre_usuario: str = Field(..., description="Nombre de usuario", max_length=50)
    foto: Optional[str] = Field(None, description="URL de la foto del usuario")
    codigo_qr: Optional[str] = Field(None, description="Código QR del usuario")
    mensaje_estado: Optional[str] = Field(None, description="Mensaje de estado del usuario", max_length=255)
    nivel_usuario: Optional[int] = Field(1, description="Nivel del usuario")

    

class PerfilUsuarioBody(BaseModel):
    data: PerfilUsuarioSchema

class PerfilUsuarioResponse(BaseModel):
    body: PerfilUsuarioBody


class FetchPerfilesUsuarioSchema(BaseModel):
    usuarios:List[PerfilUsuarioSchema]

class FetchPerfilesUsuarioSchema(BaseModel):
    perfiles: List[PerfilUsuarioSchema] = []
    total: int = 0

class FetchPerfilesUsuarioBody(BaseModel):
    data: FetchPerfilesUsuarioSchema

class FetchPerfilesUsuarioResponse(BaseModel):
    body: FetchPerfilesUsuarioBody

class FetchPerfilesUsuarioResponse(BaseModel):
    body: FetchPerfilesUsuarioBody


