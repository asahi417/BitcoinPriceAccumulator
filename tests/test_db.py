""" UnitTest """

import unittest
import btc_price
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))


class TestDB(unittest.TestCase):
    """Test for btc_price/db"""

    def test_connection(self):
        """test if connection is valid"""
        print('\ntest_connection')
        connector = btc_price.db.ConnectPSQL(host=DB_HOST, user=DB_USER, port=DB_PORT, db=DB_NAME)
        print(connector.show_table_name())
        print(connector.show_column_name('ticker'))

    # def test_show_column_name(self):
    #     """test if connection is valid"""
    #     print('\ntest_show_column_name')
    #     connector = btc_price.db.ConnectPSQL(host=DB_HOST, user=DB_USER, port=DB_PORT, db=DB_NAME)
    #     print(connector.show_table_name())


if __name__ == "__main__":
    unittest.main()
