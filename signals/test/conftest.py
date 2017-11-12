import pytest

@pytest.fixture
def config(rabbit_config):
    config = rabbit_config.copy()
    return config