from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOOKSHELF_")

    # * Опциональные переменные
    DEBUG_MODE: bool = True


configs = Configuration()

__all__ = ("configs",)
