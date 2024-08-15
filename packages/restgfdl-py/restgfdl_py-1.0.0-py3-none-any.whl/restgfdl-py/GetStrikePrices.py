from .base_api import BaseAPI

class GetStrikePrices(BaseAPI):
    def GetStrikePrices(self,exchange,instrumentType=None,product=None,expiry=None,optionType=None):
        endpoint = "GetStrikePrices/"
        params = {
            'exchange': exchange
            
        }
        if instrumentType is not None:
            params['instrumentType'] = instrumentType
        if product is not None:
            params['product'] = product
        if expiry is not None:
            params['expiry'] = expiry
        if optionType is not None:
            params['optionType'] = optionType

        return self._get(endpoint,params) 
