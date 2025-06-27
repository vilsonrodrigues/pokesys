from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="pokesys_")
    provider: str = "openai"
    model_id: str = "gpt-4.1-mini"
    executor_num_threads: int = 2
    logger_level: str = "info"

APP_CONFIG = AppConfig()
