from .base_api import BaseAPI

class GetServerInfo(BaseAPI):
    def GetServerInfo(self):
        endpoint = "GetServerInfo/"
        return self._get(endpoint) 
