import logging

from nameko.events import event_handler
from nameko.rpc import rpc

from signals import scrappers


logger = logging.getLogger(__name__)


class SignalsService:

    name = 'signals'

    @rpc
    def getAll(self, moeda):
        apisignals = scrappers.APISignals(moeda)
        signals = apisignals.run()
        return signals

    @rpc
    def getValues(self, moeda):
        apisignals = scrappers.APISignals(moeda)
        signals = apisignals.run()
        SIGNALS, CALL, PUT, NEUTRO = apisignals.process(signals, force=False)
        return {
            "CALL":CALL,
            "PUT":PUT,
            "NEUTRO":NEUTRO
        }