import time, datetime
import korean_financial_minute_data_miner.util.time

from enum import Enum

class FETCH_MODE(Enum):
    ALL_MINUTES = 1
    FIRST_RECORD = 2

DATE_FORMAT = "%Y-%m-%d"

class Fetcher():
    def __init__(self):
        import win32com.client
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")      
        self.objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

    def _set_input_value(self, code, date, fetch_mode):
        '''
        set input value to prepare a call.

        :param code: stock code
        :param date: example 20190920
        :return:
        '''
        self.objStockChart.SetInputValue(0, 'A' + code)
        self.objStockChart.SetInputValue(1, ord('1'))  # 요청 구분 '1': 기간, '2': 개수
        self.objStockChart.SetInputValue(2, date)
        self.objStockChart.SetInputValue(3, date)
        self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, ord('m'))  # 'M', 'W', 'D', 'm', 'T'
        self.objStockChart.SetInputValue(7, 1)  # period        
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가

    def _throttle(self, code):
        '''
        throttle

        :param code: this is for debugging
        :return:
        '''
        LT_NONTRADE_REQUEST = 1
        
        while True:
            remain_time = self.objCpCybos.LimitRequestRemainTime / 1000. + 0.1
            remain_count = self.objCpCybos.GetLimitRemainCount(LT_NONTRADE_REQUEST)
            
            if remain_count > 0:
                break
                
            print("{datetime} limited by 60 requests per 15 secs, processing {code}, remain_time: {remain_time}, remain_count: {remain_count}. sleeping until the throttle is cleared".format(datetime=datetime.datetime.now(), code=code, remain_time=remain_time, remain_count=remain_count))
            time.sleep(max(remain_time, 1))
        
    def _check_request_status(self):
        status = self.objStockChart.GetDibStatus()

        # -1: error, 0: normal, 1: pending
        if status == -1:
            print("GetDibStatus {}".format(status))
            return False
        
        while status == 1:
            time.sleep(1)
        
        return True

    def _fetch_by_mode(self, code, date, fetch_mode):
        '''
        fetch by minute

        :param code: stock code
        :param date: example 20190920
        :return: rows early to later
        '''
        self._throttle(code)

        self._set_input_value(code, date, fetch_mode)
        self.objStockChart.BlockRequest()

        res = []
        if not self._check_request_status():
            return res

        count_received = self.objStockChart.GetHeaderValue(3)
        if not count_received:
            print('count_received for {code} is zero, likely there was no trading for the code'.format(code=code))

        def get_date(date_v):
            '''

            :param date_v: example 20190910
            :return: iso format datetime string
            '''
            year, month, day = date_v // 10000, (date_v % 10000) // 100, date_v % 100
            t = datetime.date(year, month, day)
            return t.strftime(DATE_FORMAT)

        for r in range(count_received):
            row = []
            date_v = self.objStockChart.GetDataValue(0, r)
            time_v = self.objStockChart.GetDataValue(1, r)
            row.append(get_date(date_v))
            row.append(korean_financial_minute_data_miner.util.time.get_datetime(date_v, time_v))
            row.append(self.objStockChart.GetDataValue(2, r))
            row.append(self.objStockChart.GetDataValue(3, r))
            row.append(self.objStockChart.GetDataValue(4, r))
            row.append(self.objStockChart.GetDataValue(5, r))
            row.append(self.objStockChart.GetDataValue(6, r))
            res.append(row)

        # res so far is later to earlier
        if fetch_mode is FETCH_MODE.ALL_MINUTES:
            return res[::-1]
        elif fetch_mode is FETCH_MODE.FIRST_RECORD:
            return res[-1:]

        return res[::-1]

    def fetch_by_minute(self, code, date):
        '''
        fetch by minute

        :param code: stock code
        :param date: example 20190920
        :return: rows
        '''
        return self._fetch_by_mode(code, date, FETCH_MODE.ALL_MINUTES)

    def fetch_first_minute(self, code, date):
        '''
        fetch by minute

        :param code: stock code
        :param date: example 20190920
        :return: rows
        '''
        return self._fetch_by_mode(code, date, FETCH_MODE.FIRST_RECORD)

if __name__ == '__main__':
    fetcher = Fetcher()
    rows = fetcher.fetch_by_minute('006980', 20190919)
    for row in rows:
        print(row)