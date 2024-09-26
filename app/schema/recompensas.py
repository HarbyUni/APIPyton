from ast import List
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RecompensaSchema(BaseModel):
    id_recompensa: str = Field(..., description="ID único de la recompensa")
    nombre: str = Field(..., description="Nombre de la recompensa")
    descripcion: str = Field(..., description="Descripción de la recompensa")
    foto: Optional[str] = Field(None, description="URL de la foto de la recompensa")
    puntos_requeridos: int = Field(..., description="Puntos necesarios para canjear la recompensa")
    disponibilidad: bool = Field(..., description="Disponibilidad de la recompensa")

    class Config:
        orm_mode = True

class CreateRecompensasSchema(BaseModel):
    nombre: str = Field(..., description="Nombre de la recompensa")
    descripcion: str = Field(..., description="Descripción de la recompensa")
    foto: Optional[str] = Field(None, description="URL de la foto de la recompensa")
    puntos_requeridos: int = Field(..., description="Puntos necesarios para canjear la recompensa")
    disponibilidad: bool = Field(..., description="Disponibilidad de la recompensa")


class RecompensaBody(BaseModel):
    data: RecompensaSchema

class RecompensaResponse(BaseModel):
    body: RecompensaBody


class FetchRecompensasSchema(BaseModel):
    recompensas: List[RecompensaSchema] = []
    total: int = 0

class FetchRecompensasBody(BaseModel):
    data: FetchRecompensasSchema

class FetchRecompensasResponse(BaseModel):
    body: FetchRecompensasBody