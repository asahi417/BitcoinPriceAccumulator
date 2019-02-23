""" Definition of table and instance to connect database """

import pandas as pd
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ticker(Base):
    """Schema"""
    __tablename__ = 'ticker'
    timestamp_unix = Column(Integer, nullable=False, primary_key=True)
    product_code = Column(String, nullable=False, primary_key=True)
    tick_id = Column(Integer, nullable=False, primary_key=True)
    best_bid = Column(Float, nullable=False)
    best_ask = Column(Float, nullable=False)
    best_bid_size = Column(Float, nullable=False)
    best_ask_size = Column(Float, nullable=False)
    total_bid_depth = Column(Float, nullable=False)
    total_ask_depth = Column(Float, nullable=False)
    ltp = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    volume_by_product = Column(Float, nullable=False)


class ExchangeStatus(Base):
    """Schema"""
    __tablename__ = 'exchange_status'
    timestamp_unix = Column(Integer, nullable=False, primary_key=True)
    product_code = Column(String, nullable=False, primary_key=True)
    status = Column(String, nullable=False)


class ConnectPSQL:
    """ Create connection to postgres DB via sqlalchemy """

    def __init__(self,
                 user: str,
                 host: str,
                 port: int,
                 db: str):
        self.engine = create_engine("postgresql+psycopg2://%s@%s:%i/%s" % (user, host, port, db))
        session = sessionmaker(bind=self.engine)
        self.session = session()
        if len(self.show_table_name()) == 0:
            self.__initialize_table()

    def __initialize_table(self):
        Base.metadata.create_all(self.engine)
        self.session.commit()

    def show_table_name(self):
        sql = """SELECT relname AS table_name FROM pg_stat_user_tables"""
        df = pd.read_sql(sql, self.engine)
        return list(df.values.T[0])

    def show_column_name(self, table_name: str):
        sql = """SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = '%s'""" % table_name
        df = pd.read_sql(sql, self.engine)
        return list(df.values.T[0])

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
