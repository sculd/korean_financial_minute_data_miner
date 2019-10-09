from korean_financial_minute_data_miner import fetch
import pickle, datetime

all_fetcher = fetch.all_fetcher.ALLFetcher()
date_v = 20190919
t_before = datetime.datetime.now()
rows_by_code = all_fetcher.fetch_first_minute(date_v)
t_after = datetime.datetime.now()
dt = t_after - t_before
# about 11 minutes take
print('%d seconds took to fetch one day data for entire %d symbols '% (dt.total_seconds(), len(rows_by_code)))

# rows_by_code = all_fetcher.fetch_by_minute_today(small_sample=True)
for code, rows in rows_by_code.items():
    print('code: {code}, len: {l}'.format(code=code, l = len(rows)))

with open('ingest/sample.{date_v}.first.pickle'.format(date_v=date_v), 'wb') as handle:
    pickle.dump(rows_by_code, handle, protocol=pickle.HIGHEST_PROTOCOL)
