from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

# Importaciones internas
from src.api.db.session import get_session
from src.api.db.models import Farm, CoffeeLot
from ....schemas.schemas import (
    FarmCreate, FarmRead, FarmUpdate, FarmWithLots,
    CoffeeLotCreate, CoffeeLotRead, CoffeeLotUpdate
)

router = APIRouter(prefix="/coffee", tags=["Coffee Management"])

# ==========================================
# ENDPOINTS PARA FINCAS (FARMS)
# ==========================================

@router.post("/farms", response_model=FarmRead, status_code=status.HTTP_201_CREATED)
def create_farm(farm_in: FarmCreate, session: Session = Depends(get_session)):
    """Crea una nueva finca validando que el nombre sea único."""
    existing = session.exec(select(Farm).where(Farm.name == farm_in.name)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Esta finca ya está registrada"
        )
    
    db_farm = Farm.model_validate(farm_in)
    session.add(db_farm)
    session.commit()
    session.refresh(db_farm)
    return db_farm

@router.get("/farms", response_model=List[FarmRead])
def list_farms(
    offset: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session)
):
    """Lista todas las fincas con soporte para paginación."""
    farms = session.exec(select(Farm).offset(offset).limit(limit)).all()
    return farms

@router.get("/farms/{farm_id}", response_model=FarmWithLots)
def get_farm_detail(farm_id: int, session: Session = Depends(get_session)):
    """Obtiene el detalle de una finca incluyendo todos sus lotes asociados."""
    farm = session.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    return farm

@router.patch("/farms/{farm_id}", response_model=FarmRead)
def update_farm(farm_id: int, farm_in: FarmUpdate, session: Session = Depends(get_session)):
    """Actualiza parcialmente los datos de una finca."""
    db_farm = session.get(Farm, farm_id)
    if not db_farm:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    
    # model_dump(exclude_unset=True) asegura que solo se actualicen los campos enviados
    update_data = farm_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_farm, key, value)
    
    session.add(db_farm)
    session.commit()
    session.refresh(db_farm)
    return db_farm

@router.delete("/farms/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(farm_id: int, session: Session = Depends(get_session)):
    """Elimina una finca de la base de datos."""
    db_farm = session.get(Farm, farm_id)
    if not db_farm:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    
    session.delete(db_farm)
    session.commit()
    return None

# ==========================================
# ENDPOINTS PARA LOTES (COFFEE LOTS)
# ==========================================

@router.post("/lots", response_model=CoffeeLotRead, status_code=status.HTTP_201_CREATED)
def create_coffee_lot(lot_in: CoffeeLotCreate, session: Session = Depends(get_session)):
    """Crea un lote vinculado a una finca existente."""
    farm = session.get(Farm, lot_in.farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Finca vinculada no encontrada")
    
    db_lot = CoffeeLot.model_validate(lot_in)
    session.add(db_lot)
    session.commit()
    session.refresh(db_lot)
    return db_lot

@router.get("/lots", response_model=List[CoffeeLotRead])
def list_coffee_lots(session: Session = Depends(get_session)):
    """Lista todos los lotes registrados en el sistema."""
    lots = session.exec(select(CoffeeLot)).all()
    return lots

@router.patch("/lots/{lot_id}", response_model=CoffeeLotRead)
def update_coffee_lot(lot_id: int, lot_in: CoffeeLotUpdate, session: Session = Depends(get_session)):
    """Actualiza parcialmente los datos de un lote de café."""
    db_lot = session.get(CoffeeLot, lot_id)
    if not db_lot:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    update_data = lot_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lot, key, value)
    
    session.add(db_lot)
    session.commit()
    session.refresh(db_lot)
    return db_lot

@router.delete("/lots/{lot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coffee_lot(lot_id: int, session: Session = Depends(get_session)):
    """Elimina un lote específico."""
    db_lot = session.get(CoffeeLot, lot_id)
    if not db_lot:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    session.delete(db_lot)
    session.commit()
    return None