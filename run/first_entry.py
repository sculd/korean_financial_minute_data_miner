import datetime
import fetch.fetcher, fetch.all_fetcher
import ingest.ingest
import combine.combine
import util.dir
import util.time


def _get_first_entries_df(date_v):
    # fetch
    all_fetcher = fetch.all_fetcher.ALLFetcher()
    t_start = datetime.datetime.now()
    rows_by_code = all_fetcher.fetch_first_minute(date_v)
    t_after = datetime.datetime.now()
    dt = t_after - t_start

    # about 11 minutes take
    print('%d seconds took to fetch one day data for entire %d symbols ' % (dt.total_seconds(), len(rows_by_code)))

    # ingest into csv files
    ingest.ingest.ingest(date_v, rows_by_code, util.dir.DATA_TYPE.RAW_FIRST_MINUTE)

    # combine and get df
    return combine.combine.combine_for_date(util.time.get_date_str(date_v), util.dir.DATA_TYPE.RAW_FIRST_MINUTE)

def get_first_entries_df_today():
    '''
    return a pandas Dataframe for the first entires.
    :return:
    '''

    date_v = util.time.get_date_v_now()
    return _get_first_entries_df(date_v)
