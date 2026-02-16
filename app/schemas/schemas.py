from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

# 1. Configuración Base (TunedModel)
class TunedModel(BaseModel):
    """
    Clase base para habilitar la compatibilidad con SQLModel.
    Permite que Pydantic lea datos directamente de objetos de base de datos.
    """
    model_config = ConfigDict(from_attributes=True) # Reemplaza el antiguo orm_mode


# --- FINCAS (FARMS) ---

class FarmBase(TunedModel):
    """Define los campos comunes y validaciones básicas para una finca."""
    name: str = Field(..., example="Don Elí", max_length=100)
    zone: str = Field(..., example="Los Santos", max_length=50)
    origin: str = Field(..., example="Costa Rica", max_length=50)

class FarmCreate(FarmBase):
    """Se usa para el POST. No incluye ID porque lo genera la DB."""
    pass

class FarmRead(FarmBase):
    """Se usa para devolver datos al cliente. Incluye el ID."""
    id: int

class FarmUpdate(TunedModel):
    """Permite actualizaciones parciales. Todos los campos son opcionales."""
    name: Optional[str] = Field(None, max_length=100)
    zone: Optional[str] = Field(None, max_length=50)
    origin: Optional[str] = Field(None, max_length=50)


# --- LOTES (COFFEE LOTS) ---

class CoffeeLotBase(TunedModel):
    """Define los campos básicos de un lote de café."""
    variety: str = Field(..., example="SL28")
    process: str = Field(..., example="Honey")
    altitude: int = Field(..., ge=0, le=5000)

class CoffeeLotCreate(CoffeeLotBase):
    """Para crear un lote, necesitamos el ID de la finca vinculada."""
    farm_id: int

class CoffeeLotRead(CoffeeLotBase):
    """Respuesta estándar de un lote."""
    id: int
    farm_id: int

class CoffeeLotUpdate(TunedModel):
    """Permite modificar solo un atributo del lote (ej. solo la altitud)."""
    variety: Optional[str] = Field(None)
    process: Optional[str] = Field(None)
    altitude: Optional[int] = Field(None, ge=0, le=5000)
    farm_id: Optional[int] = None


# --- RESPUESTAS ANIDADAS (RELACIONES) ---

class FarmWithLots(FarmRead):
    """
    Devuelve una finca con toda su lista de lotes asociada.
    El nombre 'coffee_lots' debe coincidir con el Relationship de models.py.
    """
    coffee_lots: List[CoffeeLotRead] = []