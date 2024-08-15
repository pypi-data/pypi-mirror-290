from .base_api import BaseAPI

class GetLastQuoteArrayOptionGreeks(BaseAPI):
    def GetLastQuoteArrayOptionGreeks(self,exchange,tokens,detailedInfo=None):
        endpoint = "GetLastQuoteArrayOptionGreeks/"
        params = {
            'exchange': exchange,
            'tokens':tokens
            
        }
        if detailedInfo is not None:
            params['detailedInfo'] = detailedInfo
        

        return self._get(endpoint,params) 
 
