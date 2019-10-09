from enum import Enum

class DATA_TYPE(Enum):
    RAW = 1
    RAW_FIRST_MINUTE = 2
    PROCESSED = 3 # processed has empty time filled in with zero volume

def get_base_dir(data_type):
    if data_type == DATA_TYPE.RAW:
        return 'data'
    elif data_type == DATA_TYPE.RAW_FIRST_MINUTE:
        return 'data_first_minute'
    elif data_type == DATA_TYPE.PROCESSED:
        return 'data_processed'
