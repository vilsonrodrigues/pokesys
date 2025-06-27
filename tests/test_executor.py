import pytest
import concurrent.futures
from unittest.mock import patch, Mock
from pokesys.executor import Executor, scatter_gather
from pokesys.config.app import APP_CONFIG
from pokesys.logger import logger

# Fixture para limpar o singleton entre testes
@pytest.fixture(autouse=True)
def reset_executor():
    Executor._instance = None
    yield
    Executor._instance = None

# Fixture para mockar o logger
@pytest.fixture
def mock_logger():
    with patch("pokesys.executor.logger") as mock_log:
        yield mock_log

# Testes para a classe Executor
def test_executor_singleton():
    executor1 = Executor.get_instance()
    executor2 = Executor.get_instance()
    assert executor1 is executor2
    assert executor1.num_threads == APP_CONFIG.executor_num_threads

def test_scatter_gather_invalid_callables(mock_logger):
    """Testa scatter_gather com lista de callables inválida."""
    with pytest.raises(TypeError, match="`to_send` must be a non-empty list of callable objects"):
        scatter_gather([1, 2, 3])
