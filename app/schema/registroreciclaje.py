from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RegistroReciclajeSchema(BaseModel):
    id_registro: str = Field(..., description="ID único del registro de reciclaje")
    id_usuario: str = Field(..., description="ID del usuario que registró el reciclaje")
    id_material: str = Field(..., description="ID del material reciclado")
    cantidad: float = Field(..., description="Cantidad reciclada")
    fecha: datetime = Field(default_factory=datetime.now, description="Fecha del reciclaje")
    puntos: Optional[int] = Field(None, description="Puntos obtenidos por el reciclaje")

    class Config:
        orm_mode = True

class CreateRegistroReciclajeSchema(BaseModel):
    id_usuario: str = Field(..., description="ID del usuario que registró el reciclaje")
    id_material: str = Field(..., description="ID del material reciclado")
    cantidad: float = Field(..., description="Cantidad reciclada")
    fecha: datetime = Field( default_factory=datetime.now,description="Fecha del reciclaje")
    puntos: Optional[int] = Field(None, description="Puntos obtenidos por el reciclaje")


class RegistroReciclajeBody(BaseModel):
    data: RegistroReciclajeSchema

class RegistroReciclajeResponse(BaseModel):
    body: RegistroReciclajeBody


class FetchRegistroReciclajeSchema(BaseModel):
    Registros: List[RegistroReciclajeSchema] = []
    total: int = 0

class FetchRegistroReciclajeSBody(BaseModel):
    data: FetchRegistroReciclajeSchema

class FetchRegistroReciclajeResponse(BaseModel):
    body: FetchRegistroReciclajeSBody