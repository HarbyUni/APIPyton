from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ConfiguracionSchema(BaseModel):
    id_configuracion: str = Field(..., description="ID único de la configuración")
    id_centro: str = Field(..., description="ID del centro de reciclaje asociado")
    key: str = Field(..., description="Clave de configuración")
    valor: str = Field(..., description="Valor de configuración")
    ultima_actualizacion: datetime = Field(default_factory=datetime.now, description="Fecha de la última actualización")

    class Config:
        orm_mode = True
