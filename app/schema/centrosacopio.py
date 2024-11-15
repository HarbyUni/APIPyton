from pydantic import BaseModel, Field
from typing import Optional, List

class CentroAcopiochema(BaseModel):
    id: str = Field(None, description="ID único del centro de reciclaje")
    razon_social: str = Field(..., description="Razón social del centro de reciclaje")
    nit: str = Field(..., description="NIT del centro de reciclaje")
    logo: Optional[str] = Field(None, description="URL del logo del centro")
    telefono: Optional[str] = Field(None, description="Número de teléfono del centro")
    direccion: Optional[str] = Field(None, description="Dirección del centro")

    class Config:
        orm_mode = True

class CreateCentroAcopiochemaSchema(BaseModel):
    razon_social: str = Field(..., description="Razón social del centro de reciclaje")
    nit: str = Field(..., description="NIT del centro de reciclaje")
    logo: Optional[str] = Field(None, description="URL del logo del centro")
    telefono: Optional[str] = Field(None, description="Número de teléfono del centro")
    direccion: Optional[str] = Field(None, description="Dirección del centro")

class FetchCentroAcopiochemaSchema(BaseModel):
    centros: List[CentroAcopiochema] = []
    total: int = 0

class FetchCentroAcopiochemaBody(BaseModel):
    data: FetchCentroAcopiochemaSchema

class FetchCentroAcopiochemaResponse(BaseModel):
    body: FetchCentroAcopiochemaBody

class CentroAcopiochemaBody(BaseModel):
    data: CentroAcopiochema

class CentroAcopiochemaResponse(BaseModel):
    body: CentroAcopiochemaBody
