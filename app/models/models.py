from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Index

# ==== TABLA DE FINCAS ====
class Farm(SQLModel, table=True):
    __tablename__ = "farms"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True, unique=True)
    zone: str = Field(max_length=50)
    origin: str = Field(max_length=50)

    # Relación: Una finca puede tener muchos lotes (lots)
    coffee_lots: List["CoffeeLot"] = Relationship(back_populates="farm")    

# ==== TABLA DE LOTES/ORIGENES ====
class CoffeeLot(SQLModel, table=True): # Antes CoffeeOrigin
    __tablename__ = "coffee_lots" # Antes coffee_origins

    id: Optional[int] = Field(default=None, primary_key=True)
    farm_id: int = Field(foreign_key="farms.id", nullable=False)
    
    variety: str = Field(max_length=50)
    process: str = Field(max_length=30)
    altitude: int = Field(default=0, ge=0, le=5000)

    # La relación ahora suena más natural
    farm: "Farm" = Relationship(back_populates="coffee_lots")

    # Indice Compuesto para opt de produ
    __table_args__ = (
        Index("ix_origin_variety", "variety", "process"),
    )