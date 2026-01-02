from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from src.api.db.session import get_session
from src.api.db.models import Farm, CoffeeOrigin
