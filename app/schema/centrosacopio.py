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
    id: Optional[str] = Field(None, description="ID único del centro de reciclaje")
    razon_social: str = Field(..., description="Razón social del centro de reciclaje")
    nit: str = Field(..., description="NIT del centro de reciclaje")
    logo: Optional[str] = Field(None, description="URL del logo del centro")
    telefono: Optional[str] = Field(None, description="Número de teléfono del centro")
    direccion: Optional[str] = Field(None, description="Dirección del centro")


class CentroAcopiochemaBody(BaseModel):  # Extiende de BodySchema si tienes una clase base
    data: CentroAcopiochema

class CentroAcopiochemaResponse(BaseModel):  # Extiende de ResponseSchema si tienes una clase base
    body:CentroAcopiochemaBody

class FetchCentroAcopiochemaSchema(BaseModel):
    Centro: List[CentroAcopiochema] = []
    total: int = 0
    

class FetchCentroAcopiochemaBody(BaseModel):  # Extiende de BodySchema si tienes una clase base
    data: FetchCentroAcopiochemaSchema

class FetchCentroAcopiochemaResponse(BaseModel):  # Extiende de ResponseSchema si tienes una clase base
    body: FetchCentroAcopiochemaSchema

