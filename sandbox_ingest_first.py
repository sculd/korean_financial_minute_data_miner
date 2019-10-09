import pickle
import korean_financial_minute_data_miner.util.dir

rows_by_code = {}
with open('ingest/sample.20190919.first.pickle', 'rb') as handle:
    rows_by_code.update(pickle.load(handle))

korean_financial_minute_data_miner.ingest.ingest.ingest(20190919, rows_by_code, korean_financial_minute_data_miner.util.dir.DATA_TYPE.RAW_FIRST_MINUTE)

