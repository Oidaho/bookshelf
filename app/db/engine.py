from configs import configs
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# В DEBUG_MODE это SQLite. В Продакшене - PGSQL.
engine = create_async_engine(configs.database.DATABASE_URL, echo=configs.DEBUG_MODE)

AsyncSession = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

BaseORM = declarative_base()


async def get_db():
    """Функция возвращает асинхронную сессию взаимодействия с БД
    вместе с контролем интерпретатору.

    Yields:
        AsyncSession: Асинхронная сессия работы с БД.
    """
    async with AsyncSession() as session:
        yield session
