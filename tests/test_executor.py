import pytest
from unittest.mock import patch
from pokesys.executor import Executor, scatter_gather
from pokesys.config.app import APP_CONFIG

@pytest.fixture(autouse=True)
def reset_executor():
    Executor._instance = None
    yield
    Executor._instance = None

@pytest.fixture
def mock_logger():
    with patch("pokesys.executor.logger") as mock_log:
        yield mock_log

def test_executor_singleton():
    executor1 = Executor.get_instance()
    executor2 = Executor.get_instance()
    assert executor1 is executor2
    assert executor1.num_threads == APP_CONFIG.executor_num_threads

def test_scatter_gather_invalid_callables(mock_logger):
    with pytest.raises(TypeError, match="`to_send` must be a non-empty list of callable objects"):
        scatter_gather([1, 2, 3])
