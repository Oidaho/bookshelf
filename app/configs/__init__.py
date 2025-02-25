from pydantic_settings import BaseSettings, SettingsConfigDict
from .database import DatabaseConfiguration


class Projectonfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOOKSHELF_")

    # * Вложенные группы настроек
    database: DatabaseConfiguration = DatabaseConfiguration()

    # * Опциональные переменные
    DEBUG_MODE: bool = True


configs = Projectonfiguration()

__all__ = ("configs",)
