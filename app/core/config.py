from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Clase central de configuración. 
    Pydantic leerá automáticamente el archivo .env y mapeará los valores 
    validando sus tipos de datos.
    """
    
    # 1. Definición de variables con tipos y valores por defecto
    APP_NAME: str = "Coffee Tracker API"
    DEBUG: bool = Field(default=False)
    PORT: int = Field(default=8000)
    
    # 2. Variable obligatoria: si falta en el .env, la app lanzará un error inmediato.
    DATABASE_URL: str

    # 3. Configuración del comportamiento de Pydantic
    model_config = SettingsConfigDict(
        # Apunta al archivo .env en la raíz del proyecto
        env_file=".env",
        env_file_encoding="utf-8",
        # 'ignore' evita errores si hay variables extra en el .env que no usamos aquí
        extra="ignore"
    )

# Instancia única (Singleton) para ser importada en toda la aplicación
settings = Settings()