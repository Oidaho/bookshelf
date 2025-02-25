from pydantic_settings import BaseSettings, SettingsConfigDict


class Projectonfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOOKSHELF_")

    # * Опциональные переменные
    DEBUG_MODE: bool = True


configs = Projectonfiguration()

__all__ = ("configs",)
