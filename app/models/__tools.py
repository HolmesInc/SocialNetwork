import datetime


def str_to_standard_datetime(datetime_string: str) -> datetime:
    """ Convert standard string representation of datetime, like: str(datetime.datetime.now()), into datetime object

    :param datetime_string: datetime string
    :return: datetime object
    """
    return datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S.%f')


def current_time() -> datetime:
    """ Return current UTC time to use one way of getting current time across the whole app

    :return: current UTC time
    """
    return datetime.datetime.utcnow()
