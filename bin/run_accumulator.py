import btc_price
import os
import argparse
import time

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", None)


def get_options():
    parser = argparse.ArgumentParser(description='This script runs accumulation server.', formatter_class=argparse.RawTextHelpFormatter)
    share_param = {'nargs': '?', 'action': 'store', 'const': None, 'choices': None, 'metavar': None}
    parser.add_argument('--product_code', help='product_code', default='FX_BTC_JPY', type=str, **share_param)
    parser.add_argument('--freq', help='frequency of data to be stored (sec)', default=60, type=int, **share_param)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    instance = btc_price.Accumulator(user=DB_USER,
                                     host=DB_HOST,
                                     port=DB_PORT,
                                     db=DB_NAME,
                                     slack_webhool_url=SLACK_WEBHOOK)
    while True:
        try:
            instance.update(args.product_code)
            time.sleep(args.freq)
        except KeyboardInterrupt:
            instance.logger('KeyboardInterrupt', push_all=True)
            exit()



