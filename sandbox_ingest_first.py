import ingest.ingest
import pickle
import util.dir

rows_by_code = {}
with open('ingest/sample.20190919.first.pickle', 'rb') as handle:
    rows_by_code.update(pickle.load(handle))

ingest.ingest.ingest(20190919, rows_by_code, util.dir.DATA_TYPE.RAW_FIRST_MINUTE)

