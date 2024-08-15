from .base_api import BaseAPI

class GetLastQuoteShort(BaseAPI):
    def GetLastQuoteShort(self, exchange, instrument_identifier):
        endpoint = "GetLastQuoteShort/"
        params = {
            'exchange': exchange,
            'instrumentIdentifier': instrument_identifier
        }
        return self._get(endpoint, params)
