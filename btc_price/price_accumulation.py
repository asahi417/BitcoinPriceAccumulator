import pandas as pd
import traceback
from .db import ConnectPSQL, ExchangeStatus, Ticker
from .api import Public
from .util import utc_to_unix, get_logger

PRODUCT_LIST = ["BTC_JPY", "FX_BTC_JPY", "ETH_BTC"]


class Accumulator:

    __primary_key = dict()

    def __init__(self,
                 user: str,
                 host: str,
                 port: int,
                 db: str,
                 slack_webhool_url: str=None,
                 slack_log_interval: int=600):

        self.logger = get_logger(slack_webhook_url=slack_webhool_url, slack_log_interval=slack_log_interval)
        self.connection = ConnectPSQL(user=user, host=host, port=port, db=db)
        self.api = Public()

    def __insert_db(self,
                    data,
                    data_health):
        column_name = ['timestamp_unix', 'product_code', 'tick_id', 'best_bid', 'best_ask', 'best_bid_size',
                       'best_ask_size', 'total_bid_depth', 'total_ask_depth', 'ltp', 'volume', 'volume_by_product']
        df = pd.DataFrame([data], columns=column_name)
        df.to_sql(Ticker.__tablename__, self.connection.engine, if_exists='append', index=False)

        column_name = ['timestamp_unix', 'product_code', 'status']
        df = pd.DataFrame([data_health], columns=column_name)
        df.to_sql(ExchangeStatus.__tablename__, self.connection.engine, if_exists='append', index=False)

    def update(self,
               product_code: str):

        if product_code not in PRODUCT_LIST:
            self.logger('ERROR: invalid product_code: %s not in %s' % (product_code, PRODUCT_LIST), push_all=True)
            exit()

        self.logger('update db: %s' % product_code)
        if product_code not in self.__primary_key.keys():
            self.__primary_key[product_code] = dict(timestamp_utc=0)
        try:
            # price
            tick = self.api.ticker(product_code=product_code)
            product_code = tick['product_code']
            tick_id = int(tick['tick_id'])
            best_bid = float(tick['best_bid'])
            best_ask = float(tick['best_ask'])
            best_bid_size = float(tick['best_bid_size'])
            best_ask_size = float(tick['best_ask_size'])
            total_bid_depth = float(tick['total_bid_depth'])
            total_ask_depth = float(tick['total_ask_depth'])
            ltp = float(tick['ltp'])
            volume = float(tick['volume'])
            volume_by_product = float(tick['volume_by_product'])
            timestamp_utc = utc_to_unix(tick['timestamp'])

            # check duplication
            if self.__primary_key[product_code]["timestamp_utc"] >= timestamp_utc:
                self.logger(' - recent in db (%i) is later than API return (%i)'
                            % (self.__primary_key[product_code]["timestamp_utc"], timestamp_utc))
            else:
                data = [timestamp_utc, product_code, tick_id, best_bid, best_ask, best_bid_size,
                        best_ask_size, total_bid_depth, total_ask_depth, ltp, volume, volume_by_product]
                self.logger(' - price: OK')

                # health
                health = self.api.get_health(product_code=product_code)
                data_health = [timestamp_utc, product_code, health['status']]

                # update
                self.__insert_db(data, data_health)
                self.logger(' - health: OK')

                self.__primary_key[product_code]['timestamp_utc'] = timestamp_utc

        except Exception:
            error_msg = traceback.format_exc()
            self.logger('ERROR: %s' % error_msg, push_all=True)
            exit()
