import json
from marshmallow import ValidationError
from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from werkzeug import Response

from gateway.dependencies import Config
from gateway.entrypoints import http
from gateway.exceptions import SignalsNotFound

class GatewayService(object):
    """
    Service acts as a gateway to other services over http.
    """
    name = 'gateway'

    config = Config()
    signals_rpc = RpcProxy('signals')

    @http(
        "GET", "/signals/all",
        expected_exceptions=SignalsNotFound
    )
    def get_signals_all(self, request,moeda):
        """
            Gets all signals
        """
        signals = self.signals_rpc.getAll(moeda)
        return Response(signals,
            mimetype='application/json'
        )

    @http(
        "GET", "/signals/values",
        expected_exceptions=SignalsNotFound
    )
    def get_signals_values(self, request,moeda):
        """
            Gets values from signals
        """
        signals = self.signals_rpc.getValues(moeda)
        return Response(signals,
            mimetype='application/json'
        )
