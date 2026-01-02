from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Index

# TABLA DE FINCAS
class Farm(SQLModel, table=True):
    __tablename__ = "farms"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True, unique=True)
    zone: str = Field(max_length=50)
    origin: str = Field(max_length=50)

    #
    lots: List["CoffeeOrigin"] = Relationship(back_populates="farm")
    

# TABLA DE LOTES/ORIGENES
class CoffeeOrigin(SQLModel, table=True):
    __tablename__ = "coffee_origins"

    # PK: ID unico para cada origen
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Key
    farm_id: int = Field(foreign_key="farms.id", nullable=False)
    
    variety: str = Field(max_length=50)
    process: str = Field(max_length=30)
    altitude: int = Field(default=0, ge=0, le=5000)

    # Relación Inversa
    farm: Farm = Relationship(back_populates="lots")

    # Indice Compuesto para opt de produ
    __table_args__ = (
        Index("ix_origin_variety", "variety", "process")
    )