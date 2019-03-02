""" UnitTest """

import unittest
import btc_price


class TestDB(unittest.TestCase):
    """Test for btc_price/connect_psql.py"""

    def test_time(self):
        """test utc_to_unix"""
        print('\ntest_time')
        t = "2000-01-01T00:00:00.111"
        utc = btc_price.util.utc_to_unix(t)
        print(t, utc)


if __name__ == "__main__":
    unittest.main()
