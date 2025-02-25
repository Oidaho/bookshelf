from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOOKSHELF_DB_")

    # ! Обязательные переменные
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    # * Опциональные переменные
    POSTGRES_USER: str = "bookshelf"
    POSTGRES_NAME: str = "book_fund"
    POSTGRES_PORT: int = 5432

    def __init__(self, debug: bool) -> None:
        super().__init__()
        self.debug = debug

    @property
    def DATABASE_URL(self) -> str:
        # Через format читабильнее
        if self.debug:
            return "sqlite+aiosqlite:///{db_name}".format(db_name=self.POSTGRES_NAME)

        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}".format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            db_name=self.POSTGRES_NAME,
        )
