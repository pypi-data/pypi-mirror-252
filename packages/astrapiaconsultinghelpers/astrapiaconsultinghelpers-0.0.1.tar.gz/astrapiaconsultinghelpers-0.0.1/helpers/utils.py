from datetime import datetime


def get_now_date_time():
    try:
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return date_str
    except:
        raise

