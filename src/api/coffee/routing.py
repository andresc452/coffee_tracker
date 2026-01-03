from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from src.api.db.session import get_session
from src.api.db.models import Farm, CoffeeOrigin
from .schemas import FarmCreate, FarmRead, CoffeeOriginCreate, CoffeeOriginRead

router = APIRouter(prefix="/coffee", tags=["Coffee Management"])

# ==== POST - CREATE FARM ====
@router.post("/farms",response_model=FarmRead, status_code=201)
def create_farm(farm_in: FarmCreate, session: Session = Depends(get_session)):
    """Crea una finca validando que no exista el nombre."""
    
    # 1. Validar logica de negocio
    existing = session.exec(select(Farm).where(Farm.name == farm_in.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Esta finca ya está registrada")
    
    # 2. Transformar DTO -> Model
    db_farm = Farm.model_validate(farm_in)

    # 3. Persistir
    session.add(db_farm)
    session.commit()
    session.refresh(db_farm)
    
    return db_farm

# ==== POST - CREATE LOT ====
@router.post("/lots", response_model=CoffeeOriginRead, status_code=201)
def create_lot(lot_in: CoffeeOriginCreate, session: Session = Depends(get_session)):
    """Crea un lote asociado a una finca existente."""

    # 1. Validar que la finca exista
    farm = session.get(Farm, lot_in.farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    
    # 2. DTO -> Model
    db_lot = CoffeeOrigin.model_validate(lot_in)

    # 3.
    session.add(db_lot)
    session.commit()
    session.refresh(db_lot)

    return db_lot

# ==== GET - GET LOT ====
@router.get("/lots", response_model=List[CoffeeOriginRead])
def list_lots(session: Session = Depends(get_session)):
    return session.exec(select(CoffeeOrigin)).all()


