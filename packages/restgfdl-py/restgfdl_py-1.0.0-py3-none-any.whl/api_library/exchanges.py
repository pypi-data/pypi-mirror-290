from .base_api import BaseAPI

class ExchangesAPI(BaseAPI):
    def get_exchanges(self):
        endpoint = "GetExchanges/"
        return self._get(endpoint, {'xml': 'true'})
