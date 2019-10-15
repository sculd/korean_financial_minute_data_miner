import datetime
from korean_financial_minute_data_miner.fetch.fetcher import Fetcher
from korean_financial_minute_data_miner.util.time import KOREA_TIME_ZONE
from korean_financial_minute_data_miner.util import company_codes
import korean_financial_minute_data_miner.util.logging as logging

class ALLFetcher():
    def __init__(self):
        self.codes_set = company_codes.get_codes_set()
        self.fetcher = Fetcher()

    def fetch_by_minute(self, date_v, small_sample = False):
        res = {}
        codes_set = sorted(list(self.codes_set))[:100] if small_sample else self.codes_set
        print(codes_set)
        for code in codes_set:
            rows = self.fetcher.fetch_by_minute(code, date_v)
            res[code] = rows
        return res

    def fetch_by_minute_today(self, small_sample=False):
        t = datetime.datetime.utcnow()
        t.astimezone(KOREA_TIME_ZONE)
        date_v = int('%04d%02d%02d' % (t.year, t.month, t.day))
        return self.fetch_by_minute(date_v, small_sample=small_sample)

    def fetch_first_minute(self, date_v, small_sample = False):
        '''
        fetch the first entry for the given date

        The first entry is when the first trade is filled.

        :param date_v:
        :param small_sample:
        :return:
        '''
        res = {}
        codes_set = sorted(list(self.codes_set))[:100] if small_sample else self.codes_set
        logging.info('there are {l} codes to fetch'.format(l=len(codes_set)))
        for code in codes_set:
            rows = self.fetcher.fetch_first_minute(code, date_v)
            if len(rows) == 0:
                logging.info('there are zero rows for {code}, total non-empty rows so far {l}'.format(code=code, l=len(res)))
                continue
            res[code] = rows
        return res

    def fetch_first_minute_today(self, small_sample=False):
        t = datetime.datetime.utcnow()
        t.astimezone(KOREA_TIME_ZONE)
        date_v = int('%04d%02d%02d' % (t.year, t.month, t.day))
        return self.fetch_first_minute(date_v, small_sample=small_sample)

if __name__ == '__main__':
    all_fetcher = ALLFetcher()
    rows_by_code = all_fetcher.fetch_by_minute(20190919)
    for code, rows in rows_by_code.items():
        pass
