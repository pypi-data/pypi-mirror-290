from .base_api import BaseAPI

class GetInstruments(BaseAPI):
    
    
    def GetInstruments(self, exchange, product=None, instrument_type=None):
        endpoint = "GetInstruments/"
        params = {
            'exchange': exchange
        }
        if product:
            params['product'] = product
        if instrument_type:
            params['instrumentType'] = instrument_type
        return self._get(endpoint, params) 
