from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

def get_date()->str:
    '''
    format: 2023-01-01
    '''
    return datetime.today().strftime(DATE_FORMAT)

