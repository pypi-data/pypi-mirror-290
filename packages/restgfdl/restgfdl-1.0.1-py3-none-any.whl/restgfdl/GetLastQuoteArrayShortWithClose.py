from .base_api import BaseAPI

class GetLastQuoteArrayShortWithClose(BaseAPI):
    def GetLastQuoteArrayShortWithClose(self, exchange, instrument_identifiers):
        endpoint = "GetLastQuoteArrayShortWithClose/"
        params = {
            'exchange': exchange,
            'instrumentIdentifiers': instrument_identifiers
        }
        return self._get(endpoint, params)