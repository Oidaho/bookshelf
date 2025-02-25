from configs import configs
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base, sessionmaker

engine: AsyncEngine = create_async_engine(configs.database.DATABASE_URL, echo=configs.DEBUG_MODE)
LocalAsyncSession: AsyncSession = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


BaseORM = declarative_base()


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
