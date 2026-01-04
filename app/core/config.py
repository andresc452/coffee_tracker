from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Clase central de configuración. 
    Pydantic leerá automáticamente el archivo .env y mapeará los valores.
    """
    # Definimos las variables con sus tipos y validaciones
    APP_NAME: str = "Coffee Tracker API"
    DEBUG: bool = Field(default=False)
    PORT: int = Field(default=8000)
    
    # La URL es obligatoria, si no está en el .env, Pydantic lanzará error
    DATABASE_URL: str

    # Configuración de búsqueda del archivo .env
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Ignora variables extra que no estén definidas aquí
    )

# Instanciamos para que el resto de la app importe este objeto
settings = Settings()