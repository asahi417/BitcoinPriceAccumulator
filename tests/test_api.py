""" UnitTest """

import unittest
import btc_price

API = btc_price.api.Public()


class TestAPI(unittest.TestCase):
    """Test for btc_price/api"""

    def check(self, output):
        if type(output) is dict and 'status' in output.keys():
            self.assertNotEqual('error', output['status'])

    def test_initial(self):
        """test if instance is valid"""
        print('\ntest_initial')
        output = API.markets()
        self.check(output)


if __name__ == "__main__":
    unittest.main()