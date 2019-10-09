import os, datetime, dateutil.tz
import korean_financial_minute_data_miner.util.dir

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
KOREA_TIME_ZONE = dateutil.tz.tzoffset('KR', datetime.timedelta(hours=9))

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
    return t.strftime("%Y%m%d")

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

