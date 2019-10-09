import datetime, os, copy
import korean_financial_minute_data_miner.util.time
from korean_financial_minute_data_miner.util.time import DATETIME_FORMAT, KOREA_TIME_ZONE
import korean_financial_minute_data_miner.util.dir

def ingest(date_v, rows_by_code, data_type):
    '''
    given the rows by code, write them into csv.

    :param rows_by_code: map of rows keyed by code
    :return:
    '''
    date_str = korean_financial_minute_data_miner.util.time.get_date_str(date_v)
    base_dir = korean_financial_minute_data_miner.util.dir.get_base_dir(data_type)
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    dir = os.path.join(base_dir, date_str)
    if not os.path.exists(dir):
        os.mkdir(dir)
    time_str = datetime.datetime.strftime(datetime.datetime.now().astimezone(KOREA_TIME_ZONE), '%H%M')
    dir = os.path.join(base_dir, date_str, time_str)
    if not os.path.exists(dir):
        os.mkdir(dir)
    column_names = ['date', 'datetime', 'open', 'high', 'low', 'close', 'volume', 'symbol']
    for code, rows in rows_by_code.items():
        if not rows:
            continue

        # last column should be symbol
        for row in rows:
            row.append(code)

        if data_type == korean_financial_minute_data_miner.util.dir.DATA_TYPE.RAW_FIRST_MINUTE:
            rows = rows[:1]

        with open(os.path.join(dir, '{code}.csv'.format(code=code)), 'w') as outfile:
            outfile.write(','.join(column_names) + '\n')

            prev_row = copy.copy(rows[0])
            first_t = datetime.datetime.strptime(prev_row[1], DATETIME_FORMAT)
            prev_row[1] = datetime.datetime(first_t.year, first_t.month, first_t.day, 9, 0, 0, tzinfo=first_t.tzinfo).strftime(DATETIME_FORMAT)
            prev_row[-2] = 0 # zero volume

            dt_minute = datetime.timedelta(minutes=1)
            for row in rows:
                t = datetime.datetime.strptime(row[1], DATETIME_FORMAT)
                # fill in the empty (no trade happening) time buckets
                if data_type != korean_financial_minute_data_miner.util.dir.DATA_TYPE.RAW_FIRST_MINUTE:
                    while True:
                        prev_t  = datetime.datetime.strptime(prev_row[1], DATETIME_FORMAT)
                        if prev_t + dt_minute >= t:
                            break
                        prev_row[1] = (prev_t + dt_minute).strftime(DATETIME_FORMAT)
                        prev_row[-2] = 0 # zero volume
                        outfile.write(','.join(map(lambda v: str(v), prev_row))+'\n')

                outfile.write(','.join(map(lambda v: str(v), row))+'\n')
                prev_row = row
