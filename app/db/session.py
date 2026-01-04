from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

def init_db():
    # Importante: Importar modelos para que SQLModel los reconozca
    from app.models.coffee import Farm, CoffeeLot
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session