from fastapi import APIRouter
from app.api.v1.endpoints import coffee

# 1. Creamos el router principal de la Versión 1
api_router = APIRouter()

# 2. Conectamos el router de café que revisamos anteriormente
# Aquí definimos que todas las rutas dentro de 'coffee.py' 
# tendrán el prefijo '/coffee' automáticamente.
api_router.include_router(coffee.router, prefix="/coffee", tags=["Coffee Management"])

# 3. En el futuro, aquí registrarías otros módulos:
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(brew_logs.router, prefix="/brews", tags=["Brewing"])