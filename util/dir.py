from enum import Enum

class DATA_TYPE(Enum):
    RAW = 1
    PROCESSED = 2

def get_base_dir(data_type):
    if data_type == DATA_TYPE.RAW:
        return 'data'
    elif data_type == DATA_TYPE.PROCESSED:
        return 'data_processed'
