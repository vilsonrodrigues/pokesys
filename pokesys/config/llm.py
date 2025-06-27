from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="pokesys_")
    temperature: float = 0.7
    verbose: bool = True
    
LLM_CONFIG = LLMConfig()
