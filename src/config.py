from decouple import config

# 1. Definimos las variables una sola vez
DATABASE_URL = config("DATABASE_URL", cast=str, default="")
DEBUG = config("DEBUG", default=False, cast=bool)
APP_NAME = "Coffee Tracker API"

# 2. Validaciones extra
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no encontrada en el entorno")
