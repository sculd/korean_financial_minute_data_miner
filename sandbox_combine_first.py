from korean_financial_minute_data_miner.combine import combine
import korean_financial_minute_data_miner.util.dir


def run():
    df = korean_financial_minute_data_miner.combine.combine.combine_for_date('2019-09-19', korean_financial_minute_data_miner.util.dir.DATA_TYPE.RAW_FIRST_MINUTE)
    print(df.head())
    print(df.tail())
    print('All done')

if __name__ == '__main__':
    run()
