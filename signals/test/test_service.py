from marshmallow.exceptions import ValidationError
from nameko.testing.services import entrypoint_hook
from nameko.standalone.events import event_dispatcher
from nameko.testing.services import entrypoint_waiter
import pytest
from signals.service import SignalsService

@pytest.fixture
def service_container(config, container_factory):
    container = container_factory(SignalsService, config)
    container.start()
    return container

def test_get_signals(service_container):
    with entrypoint_hook(service_container, 'getAll') as getAll:
        signals = getAll('USD/JPY')
    assert type(signals) is dict

