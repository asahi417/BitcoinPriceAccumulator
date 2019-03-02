import btc_price
import os
import argparse

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))


def get_options():
    parser = argparse.ArgumentParser(description='This script produce data csv file.', formatter_class=argparse.RawTextHelpFormatter)
    share_param = {'nargs': '?', 'action': 'store', 'const': None, 'choices': None, 'metavar': None}
    parser.add_argument('--product_code', help='product_code', default='FX_BTC_JPY', type=str, **share_param)
    parser.add_argument('--out_dir', help='output directory', default='./', type=str, **share_param)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()
    if not os.path.exists(args.out_dir):
        raise ValueError('no directory found at %s' % args.out_dir)

    connector = btc_price.db.ConnectPSQL(host=DB_HOST, user=DB_USER, port=DB_PORT, db=DB_NAME)

    # slit data into 2 days span
    single_data_size = 60*60*24*2

    # get start and end unix time
    sql = """SELECT timestamp_unix FROM ticker ORDER BY timestamp_unix DESC LIMIT 1"""
    timestamp_unix_end = connector.execute_sql(sql).values[0, 0]
    sql = """SELECT timestamp_unix FROM ticker ORDER BY timestamp_unix ASC LIMIT 1"""
    timestamp_unix_start = connector.execute_sql(sql).values[0, 0]

    batch_size = int((timestamp_unix_end - timestamp_unix_start)/single_data_size)
    for n, __unix_start in enumerate(range(timestamp_unix_start, timestamp_unix_end, single_data_size)):
        __unix_end = min(__unix_start + single_data_size, timestamp_unix_end)
        print('- processing %i/%i \r' % (n, batch_size), end='', flush=True)
        out_file = os.path.join(args.out_dir, '%i_%i.csv' % (__unix_start, __unix_end))
        if os.path.exists(out_file):
            print(' - found file: %s' % out_file)
            continue
        sql = """SELECT * FROM ticker WHERE timestamp_unix > '%i' and timestamp_unix < '%i' ORDER BY timestamp_unix DESC """ \
              % (__unix_start, __unix_end)
        out = connector.execute_sql(sql)
        out.to_csv(out_file)
    print()
    print('finish')

