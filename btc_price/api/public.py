from .base import API


class Public:
    """Order API (HTTP Private API)"""

    def __init__(self, api_key=None, api_secret=None, timeout=None):
        self.api = API(api_key, api_secret, timeout)

    def markets(self):
        """Order Book
        Parameters
            product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".
        """
        endpoint = "/v1/markets"
        return self.api.request(endpoint)

    def board(self, **params):
        """Order Book
        Parameters
            product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".
        """
        endpoint = "/v1/board"
        return self.api.request(endpoint, params=params)
    
    def ticker(self, **params):
        """Ticker
        Parameters
            product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".
        """
        endpoint = "/v1/ticker"
        return self.api.request(endpoint, params=params)

    def executions(self, **params):
        """Execution History
        Parameters
            product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".
            count, before, after: See Pagination.
        """
        endpoint = "/v1/executions"
        return self.api.request(endpoint, params=params)
    
    def get_board_state(self, **params):
        """Order book status
        Parameters
            product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETC_BTC".
        """
        endpoint = "/v1/getboardstate"
        return self.api.request(endpoint, params=params)
    
    def get_health(self, **params):
        """Exchange status
        Parameters
            product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".
        Response
            status: one of the following levels will be displayed
                NORMAL: The exchange is operating.
                BUSY: The exchange is experiencing heavy traffic.
                VERY BUSY: The exchange is experiencing extremely heavy traffic. There is a possibility that orders will fail or be processed after a delay.
                STOP: The exchange has been stopped. Orders will not be accepted.
        """
        endpoint = "/v1/gethealth"
        return self.api.request(endpoint, params=params)

    def get_chats(self, **params):
        """ Chat: Get an instrument list
        Parameters
            from_date: This accesses a list of any new messages after this date.
        """
        endpoint = "/v1/getchats"
        return self.api.request(endpoint, params=params)
