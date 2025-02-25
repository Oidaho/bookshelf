from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

from .database import DatabaseConfiguration


class Projectonfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOOKSHELF_")

    # * Вложенные группы настроек
    database: Optional[DatabaseConfiguration] = None

    # * Опциональные переменные
    DEBUG_MODE: bool = True

    # ? Для передачи неких параметров во вложенные группы настроек
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.database = DatabaseConfiguration(debug=self.DEBUG_MODE)


configs = Projectonfiguration()

__all__ = ("configs",)
