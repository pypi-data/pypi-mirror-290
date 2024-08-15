from .base_api import BaseAPI

class GetLastQuote(BaseAPI):
    def GetLastQuote(self, exchange, instrument_identifier):
        endpoint = "GetLastQuote/"
        params = {
            'exchange': exchange,
            'instrumentIdentifier': instrument_identifier
        }
        return self._get(endpoint, params)