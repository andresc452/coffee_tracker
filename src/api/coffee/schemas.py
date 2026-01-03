from pydantic import BaseModel, Field
from typing import Optional, List

# Schemas para FINCAS
class FarmBase(BaseModel):
    """Atributos compartidos para Fincas"""
    name: str = Field(..., example="Don Elí",max_length=100)
    zone: str = Field(..., example="Los Santos", max_length=50)
    origin: str = Field(..., example="Costa Rica", max_length=50)

class FarmCreate(FarmBase):
    """Lo que el cliente envía al crear una finca (No incluye ID)"""
    pass

class FarmRead(FarmBase):
    """Lo que el API devuelve (Incluye ID)"""
    id: int

# Schemas para LOTES (ORIGEN)

class CoffeeOriginBase(BaseModel):
    """Atributos compartidos para Lotes"""
    variety: str = Field(..., example="SL28")
    process: str = Field(..., example="Honey")
    altitude: int = Field(..., ge=0, le=5000)

class CoffeeOriginCreate(CoffeeOriginBase):
    """Lo que el cliente envía (Necesita el ID de la finca)"""
    farm_id: int

class CoffeeOriginRead(CoffeeOriginBase):
    """Lo que la API devuelve"""
    id: int
    farm_id: int

