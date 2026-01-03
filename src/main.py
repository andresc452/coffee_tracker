from contextlib import asynccontextmanager
from fastapi import FastAPI

# Import Locales
from src.api.db.session import init_db
from src.api.coffee.routing import router as coffee_router
from src.config import APP_NAME, DEBUG

# 1. Gestion del Ciclo de Vida (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Este bloque se ejecuta antes de que la API empiece a recibir peticiones.
    Ideal para configurar la infraestructura (Base de Datos).
    """
    print(f"--- Iniciando {APP_NAME}")
    try:
        init_db() # Crea las tablas
        print("Infraestructura de Base de Datos: LISTA")
    except Exception as e:
        print(f"Error critico al inicializar la DB: {e}")

    yield # Aqui la APP permanece activa

    print(f"---  Apagado {APP_NAME}")

# 2. Instancia Principa de FastAPI
app = FastAPI(
    title=APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
    debug=DEBUG
)

# 3. Registro de Routers
app.include_router(coffee_router, prefix="/api") 

# 4. Healthcheck (Ruta de Verificacion)
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "online",
        "app": APP_NAME,
        "database": "connected"
    }