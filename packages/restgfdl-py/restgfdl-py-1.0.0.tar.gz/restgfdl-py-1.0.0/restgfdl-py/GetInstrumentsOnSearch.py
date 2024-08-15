 
from .base_api import BaseAPI

class GetInstrumentsOnSearch(BaseAPI):
    def GetInstrumentsOnSearch(self, exchange, search, detailed_info=False, instrument_type=None, option_type=None, only_active=False):
        endpoint = "GetInstrumentsOnSearch/"
        params = {
            'exchange': exchange,
            'search': search
            
        }
        if instrument_type:
            params['instrumentType'] = instrument_type
        if option_type:
            params['optionType'] = option_type
        if only_active:
            params['onlyActive'] = only_active
        if detailed_info:
            params['detailedInfo'] = detailed_info
        return self._get(endpoint, params)