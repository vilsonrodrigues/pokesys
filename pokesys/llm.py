from langchain.chat_models import init_chat_model
from pokesys.config.app import APP_CONFIG
from pokesys.config.llm import LLM_CONFIG


def get_llm(provider: str = APP_CONFIG.provider, model_id: str = APP_CONFIG.model_id):
    config = LLM_CONFIG.model_dump()
    model = init_chat_model(f"{provider}:{model_id}", **config)
    return model
