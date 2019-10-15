import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'credential.json')

from google.cloud import storage
from google.cloud.exceptions import NotFound
import korean_financial_minute_data_miner.util.logging as logging

_client = None

_BUCKET_NAME = 'stock_daily_data'
_BLOB_NAME = 'kor.daily.first.csv'

def _get_client():
    global _client
    if _client is None:
        _client = storage.Client()
    return _client

def upload(date_str):
    try:
        source_file = os.path.join('data_first_minute', date_str, 'combined.csv')
        if not os.path.exists(source_file):
            logging.warning('first minute ingest for {date_str} does not exist'.format(date_str=date_str))
            return

        client = _get_client()
        bucket = client.get_bucket(_BUCKET_NAME)
        blob = bucket.blob(_BLOB_NAME)
        blob.upload_from_filename(source_file)
        print('File {} uploaded to {}.'.format(source_file, _BLOB_NAME))
    except NotFound:
        print("Sorry, that bucket {} does not exist!".format(_BUCKET_NAME))

