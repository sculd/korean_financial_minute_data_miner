import combine.combine
import util.dir


def run():
    df = combine.combine.combine_for_date('2019-09-19', util.dir.DATA_TYPE.RAW_FIRST_MINUTE)
    print(df.head())
    print(df.tail())
    print('All done')

if __name__ == '__main__':
    run()
