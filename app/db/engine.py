from configs import configs
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine: AsyncEngine = create_async_engine(
    configs.database.DATABASE_URL,
    echo=configs.DEBUG_MODE,
    pool_pre_ping=True,
)
LocalAsyncSession: AsyncSession = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class BaseORM(AsyncAttrs, DeclarativeBase):
    pass


async def disconnect_db():
    """Закрывает подключение к БД, освобождает ресурсы."""
    await engine.dispose()


async def get_db():
    """Функция возвращает асинхронную сессию взаимодействия с БД
    вместе с контролем интерпретатору.

    Yields:
        AsyncSession: Асинхронная сессия работы с БД.
    """
    async with LocalAsyncSession() as session:
        yield session
