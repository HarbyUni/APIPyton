from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class MaterialSchema(BaseModel):
    id_material: str = Field(..., description="ID único del material")
    nombre_material: str = Field(..., description="Nombre del material")
    unidad_medida: str = Field(..., description="Unidad de medida")
    descripcion: Optional[str] = Field(None, description="Descripción del material")
    foto: Optional[str] = Field(None, description="URL de la foto del material")

    class Config:
        orm_mode = True


class CreateMaterialSchema(BaseModel):
    nombre_material: str = Field(..., description="Nombre del material")
    unidad_medida: str = Field(..., description="Unidad de medida")
    descripcion: Optional[str] = Field(None, description="Descripción del material")
    foto: Optional[str] = Field(None, description="URL de la foto del material")


class MaterialBody(BaseModel):  # Extiende de BodySchema si tienes una clase base
    data: MaterialSchema

class MaterialResponse(BaseModel):  # Extiende de ResponseSchema si tienes una clase base
    body: MaterialBody

class FetchMaterialSchema(BaseModel):
    Material: List[MaterialSchema] = []
    total: int = 0
    

class FetchMaterialBody(BaseModel):  # Extiende de BodySchema si tienes una clase base
    data: FetchMaterialSchema

class FetchMaterialResponse(BaseModel):  # Extiende de ResponseSchema si tienes una clase base
    body: FetchMaterialSchema
