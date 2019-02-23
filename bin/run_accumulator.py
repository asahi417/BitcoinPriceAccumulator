import os
import traceback
from bf_api import Public

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PORT = int(os.getenv('DB_PORT', '5000'))
DB_NAME = os.getenv('DB_NAME', 'btc_price')

API_KEY = os.getenv('API_KEY')

def main():
    Public(api_key=)


