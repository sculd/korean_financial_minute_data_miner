import os, datetime
import fetch.fetcher, fetch.all_fetcher
import ingest.ingest
import combine.combine
import util.dir
import util.time
import pandas as pd

def _save_first_entries_df(date_v):
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
    combine.combine.combine_for_date(util.time.get_date_str(date_v), util.dir.DATA_TYPE.RAW_FIRST_MINUTE)

def get_first_entries_df(date_v, force_ingest):
    '''
    Get dataframe of first entries.

    If the file does not exist, or if force_ingest is True, do fetch/ingest first.

    :param date_v:
    :param force_ingest:
    :return:
    '''
    base_dir = util.dir.get_base_dir(util.dir.DATA_TYPE.RAW_FIRST_MINUTE)
    date_str = util.time.get_date_str(date_v)
    filename_combined = os.path.join(base_dir, date_str, 'combined') + '.csv'

    if not os.path.exists(filename_combined) or force_ingest:
        _save_first_entries_df(date_v)

    df = pd.read_csv(filename_combined, index_col=['date', 'symbol'])
    df = df.loc[~df.index.duplicated(keep='first')]
    return df

def get_first_entries_df_today(force_ingest=False):
    '''
    return a pandas Dataframe for the first entires.
    :return:
    '''

    date_v = util.time.get_date_v_now()
    return get_first_entries_df(date_v, force_ingest=force_ingest)
