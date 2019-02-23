import logging
import os
from datetime import datetime
from time import time
import pytz
import slackweb
import traceback


######################
# slack notification #
######################

class SlackAlert:

    def __init__(self,
                 webhook_url: str,
                 interval: int
                 ):
        """ Slack message post instance
        To avoid error by too frequent request, buffering message for
        `post_interval_sec` seconds and send batch.

         Parameter
        ---------------
        webhool_url: str
            webhool_url of slack
        interval: int
            interval for posting log
        """

        self.__slack_log = slackweb.Slack(url=webhook_url)
        self.__interval = interval
        self.__previous_post = 0.0
        self.__msg_buffer = []

    def __call__(self,
                 msg: str,
                 push_all: bool = False):

        self.__msg_buffer.append(msg)

        if push_all or time() - self.__previous_post > self.__interval:
            self.__slack_log.notify(text='\n'.join(self.__msg_buffer))
            self.__previous_post = time()
            self.__msg_buffer = []

######################
# utility in general #
######################


def __create_log(out_file_path=None,
                 set_jst: bool=True):
    """ Logging: make logger and save at `out_file_path`.
    If `out_file_path` is None, only show in terminal and if `out_file_path` exists, delete it and make new log file
    Usage
    -------------------
    logger.info(message)
    logger.error(error)
    """

    def custom_time(*args):
        utc_dt = pytz.utc.localize(datetime.utcnow())
        my_tz = pytz.timezone('Asia/Tokyo')
        converted = utc_dt.astimezone(my_tz)
        return converted.timetuple()

    handler_stream = logging.StreamHandler()
    if out_file_path is not None:
        if os.path.exists(out_file_path):
            os.remove(out_file_path)
        handler_output = logging.FileHandler(out_file_path)
    else:
        handler_output = None

    logger = logging.getLogger(out_file_path)
    # avoid overlap logger
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("H1, %(asctime)s %(levelname)8s %(message)s")
        handler_stream.setFormatter(formatter)
        logger.addHandler(handler_stream)
        if handler_output is not None:
            handler_output.setFormatter(formatter)
            logger.addHandler(handler_output)
    if set_jst:
        logging.Formatter.converter = custom_time
    return logger


def get_logger(out_file_path=None,
               set_jst: bool=True,
               slack_webhook_url: str=None,
               slack_log_interval: int=None):
    """ return instance that is easy to get log with slack notification """
    logger = __create_log(out_file_path, set_jst)
    if slack_webhook_url is not None:
        slack = SlackAlert(webhook_url=slack_webhook_url, interval=slack_log_interval)
    else:
        slack = None

    def __log(msg: str,
              to_slack: bool = True,
              push_all: bool = False):
        logger.info(msg)
        if to_slack:
            if slack is not None:
                try:
                    slack(msg, push_all)
                except Exception:
                    msg = traceback.format_exc()
                    logger.warning(msg)
    return __log


def utc_to_unix(t):
    """ UTC Y-M-D -> UTC unix time (ignore float second point)
    t = "2000-01-01T00:00:00.111" """
    t = t.split('.')[0]
    dt = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
    tz = pytz.timezone('UTC')
    dt = tz.localize(dt)
    unix_time = int(dt.timestamp())
    return unix_time
