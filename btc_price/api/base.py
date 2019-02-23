import json
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
import traceback


class API:

    def __init__(self, api_key, api_secret, timeout):
        self.api_url = "https://bf_api.bitflyer.jp"
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout

    def request(self,
                endpoint,
                method="GET",
                params=None):

        try:
            url = '%s%s' % (self.api_url, endpoint)
            auth_header = None

            if method == "POST":
                body = json.dumps(params)
            else:
                body = "?%s" % urlencode(params) if params else ""

            if self.api_key and self.api_secret:
                access_timestamp = str(time.time())
                api_secret = str.encode(self.api_secret)
                text = str.encode(access_timestamp + method + endpoint + body)
                access_sign = hmac.new(api_secret,
                                       text,
                                       hashlib.sha256).hexdigest()
                auth_header = {
                    "ACCESS-KEY": self.api_key,
                    "ACCESS-TIMESTAMP": access_timestamp,
                    "ACCESS-SIGN": access_sign,
                    "Content-Type": "application/json"
                }

            with requests.Session() as s:
                if auth_header:
                    s.headers.update(auth_header)

                if method == "GET":
                    response = s.get(url, params=params, timeout=self.timeout)
                else:  # method == "POST":
                    response = s.post(url, data=json.dumps(params), timeout=self.timeout)

            content = response.content.decode("utf-8")
            if content in ['[]', '']:
                content = dict()
            else:
                content = json.loads(response.content.decode("utf-8"))

            if response.status_code == 200:
                if type(content) == dict:
                    content['status_code'] = 200
            return content

        except Exception:
            return dict(status="error", error_message=traceback.format_exc())

    def check_keys(self):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()


class AuthException(Exception):

    def __init__(self):
        msg = "Please specify your valid API Key and API Secret."
        super(AuthException, self).__init__(msg)
