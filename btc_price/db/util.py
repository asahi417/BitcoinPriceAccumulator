"""
Module for database operation
"""

import pandas as pd
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductCode(Base):
    """Schema"""
    __tablename__ = 'product_code'
    product_code_id = Column(Integer, nullable=False, primary_key=True)
    product_code = Column(String, nullable=False)


class Ticker(Base):
    """Schema"""
    __tablename__ = 'ticker'
    unix_time = Column(Integer, nullable=False, primary_key=True)
    product_code_id = Column(Integer, nullable=False, primary_key=True)
    tick_id = Column(Integer, nullable=False, primary_key=True)
    sample_period = Column(Integer, nullable=False, primary_key=True)
    best_bid = Column(Float, nullable=False)
    best_ask = Column(Float, nullable=False)
    best_bid_size = Column(Float, nullable=False)
    best_ask_size = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    volume_by_product = Column(Float, nullable=False)


class ExchangeStatus(Base):
    """Schema"""
    __tablename__ = 'exchange_status'
    unix_time = Column(Integer, nullable=False, primary_key=True)
    tick_id = Column(Integer, nullable=False, primary_key=True)
    status = Column(String, nullable=False)


class ConnectPSQL:
    """
    instance to connect postgres DB via sqlalchemy
    """

    def __init__(self,
                 user: str,
                 host: str,
                 port: int,
                 db: str):
        self.engine = create_engine("postgresql+psycopg2://%s@%s:%i/%s" % (user, host, port, db))
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def db_initializer(self):
        Base.metadata.create_all(self.engine)
        self.session.commit()

        # initialize `ProductCode`
        tmp = [
            [0, "BTC_JPY"],
            [1, "FX_BTC_JPY"],
            [2, "ETH_BTC"],
            [3, "BTCJPY28APR2017"],
            [4, "BTCJPY05MAY2017"],
            [5, "BTC_USD"]
        ]
        target = pd.DataFrame(tmp, columns=["product_code_id", "product_code"])
        target.to_sql(ProductCode.__tablename__, self.engine, if_exists='replace', index=False)

    def show_table_name(self):
        sql = """SELECT relname AS table_name FROM pg_stat_user_tables"""
        return pd.read_sql(sql, self.engine)

    # def get_historical_data(self,
    #                         period,
    #                         limit=10,
    #                         begin: int = None,
    #                         end: int = None):
    #     """ get latest historical data
    #     return pandas data-frame with colmuns:
    #     ['ticker_index', 'close_unix_time', 'sample_period', 'open_price', 'high_price', 'low_price', 'close_price',
    #     'volume']
    #     """
    #     query = "select * from price where sample_period = %i" % period
    #     if begin is not None:
    #         query += ' and close_unix_time > %i' % begin
    #     if end is not None:
    #         query += ' and close_unix_time < %i' % end
    #     query += " order by close_unix_time desc"
    #     if begin is None or end is None:
    #         query += " limit %i;" % limit
    #     return pd.read_sql(query, self.engine)
