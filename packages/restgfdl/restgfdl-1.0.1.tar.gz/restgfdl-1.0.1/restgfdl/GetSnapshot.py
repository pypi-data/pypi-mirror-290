from .base_api import BaseAPI

class GetSnapshot(BaseAPI):
    def GetSnapshot(self, exchange, periodicity, period, instrument_identifiers, is_short_identifiers=None):
        endpoint = "GetSnapshot/"
        params = {
            'exchange': exchange,
            'periodicity': periodicity,
            'period': period,
            'instrumentIdentifiers': instrument_identifiers
        }
        if is_short_identifiers is not None:
            params['isShortIdentifiers'] = is_short_identifiers
        return self._get(endpoint, params)

