from .base_api import BaseAPI

class GetExchanges(BaseAPI):
    def GetExchanges(self):
        endpoint = "GetExchanges/"
        return self._get(endpoint) 
