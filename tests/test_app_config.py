import os
from pokesys.config.app import AppConfig


def test_app_config_defaults():
    config = AppConfig()
    assert config.provider == "openai"
    assert config.model_id == "gpt-4.1-mini"
    assert config.executor_num_threads == 2
    assert config.logger_level == "info"


def test_app_config_from_env(monkeypatch):
    monkeypatch.setenv("pokesys_provider", "vllm")
    monkeypatch.setenv("pokesys_model_id", "bge-large")
    monkeypatch.setenv("pokesys_executor_num_threads", "8")
    monkeypatch.setenv("pokesys_logger_level", "debug")

    config = AppConfig()
    assert config.provider == "vllm"
    assert config.model_id == "bge-large"
    assert config.executor_num_threads == 8
    assert config.logger_level == "debug"
