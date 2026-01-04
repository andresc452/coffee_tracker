from contextlib import asynccontextmanager
from fastapi import FastAPI

# Importaciones Locales
from src.api.db.session import init_db
from app.api.v1.endpoints.routing import router as coffee_router
from app.core.config import settings  # 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"--- Iniciando {settings.APP_NAME}") # 
    try:
        init_db() #
        print("Infraestructura de Base de Datos: LISTA")
    except Exception as e:
        print(f"Error crítico al inicializar la DB: {e}")
    yield
    print(f"--- Apagado {settings.APP_NAME}") # 

app = FastAPI(
    title=settings.APP_NAME, # 
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.DEBUG # 
)

app.include_router(coffee_router, prefix="/api") #

@app.get("/health", tags=["System"])
async def health_check():
    # Asegúrate de usar ':' para separar clave de valor
    return {
        "status": "online",
        "app": settings.APP_NAME, # 
        "database": "connected"
    }