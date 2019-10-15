import yaml, datetime
from pytz import timezone


def load(filename):
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg

def get_tz(cfg):
    return timezone(cfg['market']['timezone'])

def _get_tz_utcoffset_hours(cfg):
    tz = timezone(cfg['market']['timezone'])
    td = tz.utcoffset(datetime.datetime.utcnow())
    return td.seconds // 3600

def get_day_data_ingest_start(cfg):
    '''
    Get datetime.time for ingest start.

    :param cfg:
    :return:
    '''
    t = datetime.datetime.strptime(cfg['market']['daydataingeststart'], '%H:%M:%S')
    return datetime.time(t.hour, t.minute, t.second, tzinfo=get_tz(cfg))
