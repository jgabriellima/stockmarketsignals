import json
from mock import call

class TestGetSignals(object):
    def test_get_signals(self, gateway_service, web_session):
        response = web_session.get('/signals')
        # assert response.status_code == 200
        # assert gateway_service.signals_rpc.getAll("USD/JPY")
        # assert type(response.json()) is dict

    def test_get_signals_values(self, gateway_service, web_session):
        response = web_session.get('/signals/values')
        # assert response.status_code == 200
        # assert gateway_service.signals_rpc.getValues("USD/JPY")
        # assert type(response.json()) is dict