from contextlib import asynccontextmanager
from fastapi import FastAPI

# 1. Importaciones Locales ajustadas a la nueva estructura
from app.db.session import init_db
from app.api.v1.api import api_router  # Conectamos el router central v1
from app.core.config import settings

# 2. Gestión del Ciclo de Vida (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Se ejecuta al arrancar la aplicación. 
    Garantiza que las tablas existan antes de recibir peticiones.
    """
    print(f"--- Iniciando {settings.APP_NAME}")
    try:
        init_db() 
        print("Infraestructura de Base de Datos: LISTA")
    except Exception as e:
        print(f"Error crítico al inicializar la DB: {e}")
    
    yield # La aplicación permanece encendida
    
    print(f"--- Apagado {settings.APP_NAME}")

# 3. Instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.DEBUG
)

# 4. Registro de Routers
# Ahora usamos el api_router que agrupa todos los endpoints v1
app.include_router(api_router, prefix="/api/v1")

# 5. Healthcheck
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "database": "connected"
    }