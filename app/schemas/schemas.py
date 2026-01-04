from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

# Configuración base para todos los Schemas
class TunedModel(BaseModel):
    # Permite que Pydantic lea modelos de base de datos (antes llamado orm_mode)
    model_config = ConfigDict(from_attributes=True)


# --- FINCAS (FARMS) ---

class FarmBase(TunedModel):
    """Atributos comunes para Fincas"""
    name: str = Field(..., example="Don Elí", max_length=100)
    zone: str = Field(..., example="Los Santos", max_length=50)
    origin: str = Field(..., example="Costa Rica", max_length=50)

class FarmCreate(FarmBase):
    """Esquema de Creación: No requiere ID porque la DB lo genera."""
    pass

class FarmRead(FarmBase):
    """Esquema de Lectura: Devuelve los datos básicos + el ID."""
    id: int

class FarmUpdate(TunedModel):
    """
    Esquema de Actualización:
    Todos los campos son opcionales (None). Si el usuario solo envía 'zone',
    Pydantic ignorará el resto y no sobreescribirá con datos vacíos.
    """
    name: Optional[str] = Field(None, max_length=100)
    zone: Optional[str] = Field(None, max_length=50)
    origin: Optional[str] = Field(None, max_length=50)

# --- LOTES (COFFEE ORIGIN) ---

class CoffeeLotBase(TunedModel):
    """Atributos comunes para Lotes"""
    variety: str = Field(..., example="SL28")
    process: str = Field(..., example="Honey")
    altitude: int = Field(..., ge=0, le=5000)

class CoffeeLotCreate(CoffeeLotBase):
    """Requiere el farm_id para vincular el lote a una finca."""
    farm_id: int

class CoffeeLotRead(CoffeeLotBase):
    id: int
    farm_id: int

class CoffeeLotUpdate(TunedModel):
    """Permite cambiar variedad, proceso o altitud de forma independiente."""
    variety: Optional[str] = Field(None)
    process: Optional[str] = Field(None)
    altitude: Optional[int] = Field(None, ge=0, le=5000)
    farm_id: Optional[int] = None # Permite mover el lote a otra finca si es necesario

# --- RESPUESTAS ANIDADAS (RELACIONES) ---

class FarmWithLots(FarmRead):
    """
    Respuesta detallada: Devuelve la finca y busca automáticamente 
    sus lotes asociados.
    """
    # IMPORTANTE: El nombre 'coffee_lots' debe coincidir con el 'Relationship' en models.py
    coffee_lots: List[CoffeeLotRead] = []