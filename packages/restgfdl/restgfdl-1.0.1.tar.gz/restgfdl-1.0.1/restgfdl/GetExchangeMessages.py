from .base_api import BaseAPI

class GetExchangeMessages(BaseAPI):
    def GetExchangeMessages(self,exchange):
        endpoint = "GetExchangeMessages/"
        params = {
            'exchange': exchange
        }
        

        return self._get(endpoint,params) 