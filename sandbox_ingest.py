import ingest.ingest
import pickle

rows_by_code = {}
with open('ingest/sample.pickle', 'rb') as handle:
    rows_by_code.update(pickle.load(handle))

ingest.ingest.ingest(20190920, rows_by_code)
