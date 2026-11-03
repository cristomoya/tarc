# db.py — pool de conexiones async con SQLAlchemy + asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import settings

engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    # PostgreSQL cierra las sesiones inactivas (idle_session_timeout = 30 min): sin esto el pool
    # entrega conexiones ya cerradas y la primera consulta tras un rato sin uso falla con un 500.
    pool_pre_ping=True,
    pool_recycle=1200,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
