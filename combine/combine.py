import os
import pandas as pd
import util.time, util.dir
from concurrent.futures import ThreadPoolExecutor

_THREAD_LEN_FILES = 100

def _combine_all_in_filenames(filenames):
    df_combined = pd.DataFrame()
    cnt = 0
    for filename in filenames:
        print('combining {filename} {cnt}th'.format(filename=filename, cnt=cnt))
        # change_close misses sign, thus drop
        df = pd.read_csv(filename, converters={'symbol': str})
        df['datetime'] = pd.to_datetime(df['datetime'], format=util.time.DATETIME_FORMAT)
        df = df.set_index('datetime')
        df_combined = df_combined.append(df)
        cnt += 1
    return df_combined

def _combine_all_in(dir):
    '''
    Combine csv file per company into single csv file.
    '''

    filenames = []
    for filename in os.listdir(dir):
        if not filename.endswith('.csv'):
            continue
        full_filename = os.path.join(dir, filename)
        filenames.append(full_filename)

    executor = ThreadPoolExecutor(max_workers=100)
    futures = []
    i = 0
    while i < len(filenames):
        futures.append(executor.submit(_combine_all_in_filenames, filenames[i:i+_THREAD_LEN_FILES]))
        i += _THREAD_LEN_FILES

    df_combined = pd.DataFrame()
    for future in futures:
        df = future.result()
        df_combined = df_combined.append(df)

    executor.shutdown(wait=True)
    return df_combined

def combine_for_date(date_str, data_type):
    '''
    combine all the files ingested most recently, into single csv file.

    :param date_str: e.g. 2019-09-19
    :return: pandas dataframe
    '''
    latest = util.time.get_latest_time_v(date_str, data_type)
    if latest == 0:
        return pd.DataFrame()
    base_dir = util.dir.get_base_dir(data_type)
    df = _combine_all_in(os.path.join(base_dir, date_str, latest))
    df.to_csv(os.path.join(base_dir, date_str, 'combined') + '.csv')
    return df
