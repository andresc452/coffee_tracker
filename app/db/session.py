from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# 1. Configuración del Motor (Engine)
# Usamos las variables validadas en app.core.config
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,      # Muestra el SQL generado en consola si DEBUG es True
    pool_pre_ping=True,       # Verifica la conexión antes de usarla (evita conexiones muertas)
    pool_size=5,              # Número de conexiones base
    max_overflow=10           # Conexiones extra si hay mucha demanda
)

# 2. Inicialización de la Base de Datos
def init_db():
    """
    Crea las tablas físicamente en la base de datos basándose en los modelos definidos.
    """
    # IMPORTANTE: Debemos importar los modelos aquí para que SQLModel los registre
    # antes de llamar a create_all
    from app.models.models import Farm, CoffeeLot
    SQLModel.metadata.create_all(engine)

# 3. Dependencia de Sesión
def get_session():
    """
    Generador que provee una sesión de base de datos para cada petición API
    y la cierra automáticamente al terminar.
    """
    with Session(engine) as session:
        yield session