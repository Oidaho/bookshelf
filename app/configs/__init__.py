from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import DatabaseConfiguration


class Projectonfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOOKSHELF_")

    # * Вложенные группы настроек
    database: DatabaseConfiguration

    # * Опциональные переменные
    DEBUG_MODE: bool = True

    # ? Для передачи неких параметров во вложенные группы настроек
    def __init__(self) -> None:
        super().__init__()
        self.database = DatabaseConfiguration(self.DEBUG_MODE)


configs = Projectonfiguration()

__all__ = ("configs",)
