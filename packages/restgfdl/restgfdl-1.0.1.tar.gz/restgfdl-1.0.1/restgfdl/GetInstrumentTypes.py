from .base_api import BaseAPI

class GetInstrumentTypes(BaseAPI):
    def GetInstrumentTypes(self,exchange):
        endpoint = "GetInstrumentTypes/"
        params = {
            'exchange': exchange
            
        }
        

        return self._get(endpoint,params)  
