from sqlmodel import create_engine, Session, SQLModel

from src.config import DATABASE_URL, DEBUG

# 1. El Motor (Engine)
engine = create_engine(
    DATABASE_URL,
    echo=DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# 2. El Inicializador (init_db)
def init_db():
    from . import models
    SQLModel.metadata.create_all(engine)

# 3. El Generador de Sesiones (get_session)
def get_session():
    with Session(engine) as session:
        yield session