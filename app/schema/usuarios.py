from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class UsuarioSchema(BaseModel):
    id: str = Field(..., description="ID único del usuario")
    nombres: str = Field(..., description="Nombres del usuario", max_length=100)
    apellidos: str = Field(..., description="Apellidos del usuario", max_length=100)
    fecha_nacimiento: datetime = Field(..., description="Fecha de nacimiento del usuario")
    edad: Optional[int] = Field(None, description="Edad del usuario")
    genero: Optional[str] = Field(None, description="Género del usuario")
    email: str = Field(..., description="Correo electrónico del usuario")
    hashed_password: Optional[str] = Field(None, description="Contraseña hasheada")
    ocupacion: Optional[str] = Field(None, description="Ocupación del usuario")
    telefono: Optional[str] = Field(None, description="Número telefónico del usuario")
    pais: Optional[str] = Field(None, description="País del usuario")
    ciudad: Optional[str] = Field(None, description="Ciudad del usuario")
    fecha_registro: datetime = Field(default_factory=datetime.now, description="Fecha de registro del usuario")
    tipo_usuario: Optional[str] = Field(None, description="Tipo de usuario")

    class Config:
        orm_mode = True


class CreateUsuarioSchema(BaseModel):
    id: Optional[str] = Field(None, description="ID único del usuario")
    nombres: str = Field(..., description="Nombres del usuario", max_length=100)
    apellidos: str = Field(..., description="Apellidos del usuario", max_length=100)
    fecha_nacimiento: datetime = Field(..., description="Fecha de nacimiento del usuario")
    edad: Optional[int] = Field(None, description="Edad del usuario")
    genero: Optional[str] = Field(None, description="Género del usuario")
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario", min_length=6)
    ocupacion: Optional[str] = Field(None, description="Ocupación del usuario")
    telefono: Optional[str] = Field(None, description="Número telefónico del usuario")
    pais: Optional[str] = Field(None, description="País del usuario")
    ciudad: Optional[str] = Field(None, description="Ciudad del usuario")
    fecha_registro: datetime = Field(default_factory=datetime.now, description="Fecha de registro del usuario")
    tipo_usuario: Optional[str] = Field(None, description="Tipo de usuario")


class UsuarioBody(BaseModel):  # Extiende de BodySchema si tienes una clase base
    data: UsuarioSchema

class UsuarioResponse(BaseModel):  # Extiende de ResponseSchema si tienes una clase base
    body: UsuarioBody

class FetchUsuariosSchema(BaseModel):
    usuarios: List[UsuarioSchema] = []
    total: int = 0
    

class FetchUsuariosBody(BaseModel):  # Extiende de BodySchema si tienes una clase base
    data: FetchUsuariosSchema

class FetchUsuariosResponse(BaseModel):  # Extiende de ResponseSchema si tienes una clase base
    body: FetchUsuariosBody
