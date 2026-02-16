from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Index

# ==== TABLA DE FINCAS (Entidad Principal) ====
class Farm(SQLModel, table=True):
    __tablename__ = "farms"

    # Atributos físicos en la base de datos
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True, unique=True) # Unicidad para evitar duplicados
    zone: str = Field(max_length=50)
    origin: str = Field(max_length=50)

    # Relación lógica (Python): Una finca tiene muchos lotes
    # Se usa back_populates para sincronizar ambos lados de la relación
    coffee_lots: List["CoffeeLot"] = Relationship(back_populates="farm")    

# ==== TABLA DE LOTES (Entidad Relacionada) ====
class CoffeeLot(SQLModel, table=True): 
    __tablename__ = "coffee_lots"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Llave Foránea: El ancla física con la tabla farms
    farm_id: int = Field(foreign_key="farms.id", nullable=False)
    
    variety: str = Field(max_length=50)
    process: str = Field(max_length=30)
    altitude: int = Field(default=0, ge=0, le=5000)

    # Relación lógica (Python): Muchos lotes pertenecen a una finca
    farm: "Farm" = Relationship(back_populates="coffee_lots")

    # Configuración avanzada de la tabla (Indices)
    __table_args__ = (
        # Optimiza búsquedas frecuentes por variedad y proceso
        Index("ix_lot_variety_process", "variety", "process"),
    )