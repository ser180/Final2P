from pydantic import BaseModel, Field
from enum import Enum

class Clasificaciones(str, Enum):
    A = "A"
    B = "B"
    C = "C"

class modelPelicula(BaseModel):
    Titulo: str = Field(..., min_length=2, description="Título mínimo 2 letras")
    Genero: str = Field(..., min_length=4, description="Género mínimo 4 letras")
    año: int = Field(..., ge=1000, le=9999, description="Año debe tener 4 dígitos")
    Clasificacion: Clasificaciones

    class Config:
        json_schema_extra = {
            "example": {
                "Titulo": "Godzilla",
                "Genero": "Acción",
                "año": 2000,
                "Clasificacion": "B"
            }
        }

class TokenData(BaseModel):
    id: str

