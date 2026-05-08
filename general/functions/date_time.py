from datetime import datetime, timedelta
from random import randint

import pytz


UTC = pytz.UTC
BRAZIL_TIMEZONE = pytz.timezone('America/Sao_Paulo')
MIN_ADD_MINUTES = 5
MAX_ADD_MINUTES = 10


def get_utc_time_now() -> datetime:
    dt = datetime.now(tz=UTC)

    return dt


def get_brazil_time_now() -> datetime:
    dt = get_utc_time_now()
    dt = utc_to_brazil_datetime(dt)

    return dt


def datetime_to_string(dt: datetime) -> str:
    if isinstance(dt, datetime):
        dt = dt.strftime("%d/%m/%Y %H:%M:%S")

    return dt


def utc_to_brazil_datetime(dt: datetime) -> datetime:
    dt = dt.astimezone(BRAZIL_TIMEZONE)

    return dt


def brazil_to_utc_datetime(dt: datetime) -> datetime:
    dt = replace_tzinfo(dt)
    delta = timedelta(hours=3)

    return dt + delta


def add_random_minutes_now(dt: datetime = None) -> datetime:
    if not dt:
        dt = get_brazil_time_now()
    dt = replace_tzinfo(dt)
    minutes = randint(MIN_ADD_MINUTES, MAX_ADD_MINUTES)
    print(f"Adding {minutes} minutes")

    return dt + timedelta(minutes=minutes)


def replace_tzinfo(dt: datetime) -> datetime:

    return dt.replace(tzinfo=UTC)


def get_last_hour() -> datetime:
    now = datetime.now()
    next_hour = now.replace(microsecond=0, second=0, minute=0)

    return next_hour


def get_midnight_hour(get_yesterday: bool = False) -> datetime:
    now = get_brazil_time_now()
    midnight_hour = now.replace(microsecond=0, second=0, minute=0, hour=3)

    if get_yesterday:
        midnight_hour = midnight_hour - timedelta(days=1)

    return midnight_hour


def adjust_season_datetime(input_datetime: datetime) -> datetime:
    '''Adiciona 1 ano ao datetime fornecido se a data já passou em relação ao
    momento atual.
    Caso contrário, retorna o mesmo datetime sem alterações.
    '''

    # print('START ADJUST_DATETIME:', input_datetime)
    now = get_brazil_time_now()
    if replace_tzinfo(input_datetime) <= now:
        try:
            new_year = input_datetime.year + 1
            if new_year < now.year:
                new_year = now.year
            input_datetime = input_datetime.replace(year=new_year)
            input_datetime = adjust_season_datetime(input_datetime)
        except ValueError:
            # Trata datas como 29 de fevereiro em anos não bissextos
            input_datetime = input_datetime + timedelta(days=366)
            input_datetime = adjust_season_datetime(input_datetime)
    # print('END ADJUST_DATETIME:', input_datetime)

    return input_datetime


if __name__ == '__main__':
    print('UTC', get_utc_time_now())
    print('BRAZIL', get_brazil_time_now())

    dt = get_utc_time_now()
    dt = utc_to_brazil_datetime(dt)
    dt = utc_to_brazil_datetime(dt)
    print('BRAZIL', dt)
