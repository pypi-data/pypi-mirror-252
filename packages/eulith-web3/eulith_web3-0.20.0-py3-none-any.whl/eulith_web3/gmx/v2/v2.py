from eulith_web3.eulith_service import EulithService
from eulith_web3.exceptions import EulithRpcException


class GmxV2Client:
    def __init__(self, eulith_service: EulithService):
        self.eulith_service = eulith_service

    def get_tickers(self):
        response, error = self.eulith_service.get_gmx_v2_tickers()
        if error:
            raise EulithRpcException(error)
        return response

    def get_funding_rates(self):
        response, error = self.eulith_service.get_gmx_v2_funding_rates()
        if error:
            raise EulithRpcException(error)
        return response

