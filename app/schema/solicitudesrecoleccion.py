from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SolicitudRecoleccionSchema(BaseModel):
    id_solicitud: str = Field(..., description="ID único de la solicitud de recolección")
    id_usuario: str = Field(..., description="ID del usuario que realiza la solicitud")
    fecha_recoleccion: Optional[datetime] = Field(None, description="Fecha solicitada para la recolección")
    direccion: str = Field(..., description="Dirección de recolección")
    codigo_qr: Optional[str] = Field(None, description="Código QR generado")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")
    status: Optional[str] = Field(None, description="Estado de la solicitud")
    id_centro: Optional[str] = Field(None, description="ID del centro de reciclaje asociado")
    id_recolector: Optional[str] = Field(None, description="ID del recolector asignado")

    class Config:
        orm_mode = True
