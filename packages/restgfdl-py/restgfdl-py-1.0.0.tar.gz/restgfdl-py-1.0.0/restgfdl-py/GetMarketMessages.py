from .base_api import BaseAPI

class GetMarketMessages(BaseAPI):
    def GetMarketMessages(self,exchange):
        endpoint = "GetMarketMessages/"
        params = {
            'exchange': exchange
            
        }
        

        return self._get(endpoint,params)  
