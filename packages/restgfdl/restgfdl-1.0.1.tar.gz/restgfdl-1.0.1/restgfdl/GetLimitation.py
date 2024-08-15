from .base_api import BaseAPI

class GetLimitation(BaseAPI):
    def GetLimitation(self):
        endpoint = "GetLimitation/"
        

        return self._get(endpoint) 
