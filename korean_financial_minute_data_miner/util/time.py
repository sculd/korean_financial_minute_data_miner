import os, datetime, dateutil.tz
import pytz
import korean_financial_minute_data_miner.util.dir
from pytz import timezone


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
KOREA_TIME_ZONE = timezone("Asia/Seoul")


def get_utcnow():
    tz_utc = pytz.utc
    return tz_utc.localize(datetime.datetime.utcnow())

def get_today_str_tz():
    return str(get_utcnow().astimezone(KOREA_TIME_ZONE).date())

def get_now_tz():
    '''
    get datetime.time of now in korean time zone.
    :return:
    '''
    now_tz = get_utcnow().astimezone(KOREA_TIME_ZONE)
    return datetime.time(now_tz.hour, now_tz.minute, now_tz.second, tzinfo=KOREA_TIME_ZONE)

def time_diff_seconds(t1, t2):
    '''
    Get datetime.timedelta between two datetime.time

    :param t1:
    :param t2:
    :return:
    '''
    today = datetime.date.today()
    dt1, dt2 = datetime.datetime.combine(today, t1), datetime.datetime.combine(today, t2)
    tf = dt1 - dt2
    return tf.days * 24 * 3600 + tf.seconds

def get_date_str(date_v):
    '''
    from integer to iso format

    :param date_v: e.g. 20190919
    :return: 20190919 -> 2019-09-19
    '''
    year, month, day = date_v // 10000, (date_v % 10000) // 100, date_v % 100
    return '%04d-%02d-%02d' % (year, month, day)

def get_datetime(date_v, time_v):
    '''

    :param date_v: example 20190910
    :param time_v: example 0931
    :return: iso format datetime string
    '''
    year, month, day = date_v // 10000, (date_v % 10000) // 100, date_v % 100
    hour, minute = time_v // 100, time_v % 100
    t = datetime.datetime(year, month, day, hour, minute, tzinfo=KOREA_TIME_ZONE)
    return t.strftime(DATETIME_FORMAT)

def get_date_v_now():
    '''
    get date_v of current time
    :return: 2019-09-19 -> 20190919
    '''
    t = datetime.datetime.now().astimezone(KOREA_TIME_ZONE)
    return int(t.strftime("%Y%m%d"))

def get_latest_time_v(date_str, data_type):
    '''
    for the given date, get the latest time_v

    :param date_str: e.g. 2019-09-19
    :return: latest time_v (int)
    '''
    latest = '0'
    base_dir = korean_financial_minute_data_miner.util.dir.get_base_dir(data_type)

    for time_str in os.listdir(os.path.join(base_dir, date_str)):
        if not os.path.isdir(os.path.join(base_dir, date_str, time_str)): continue
        if int(time_str) <= int(latest): continue
        latest = time_str
    return latest

