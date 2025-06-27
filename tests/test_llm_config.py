from pokesys.config.llm import LLMConfig


def test_llm_config_defaults():
    config = LLMConfig()
    assert config.temperature == 0.7
    assert config.verbose is True


def test_llm_config_from_env(monkeypatch):
    monkeypatch.setenv("pokesys_temperature", "0.1")
    monkeypatch.setenv("pokesys_verbose", "false")

    config = LLMConfig()
    assert config.temperature == 0.1
    assert config.verbose is False
