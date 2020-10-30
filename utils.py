import re
from datetime import datetime, timedelta

from data import USERS

TIME_REGEX = re.compile(r"(\d{1,2})[hH](\d{1,2})?")


def parse_hour(string: str, now=datetime.utcnow()) -> datetime:
    match = TIME_REGEX.fullmatch(string)
    if match is None:
        return None
    else:
        hours, minutes = match.groups()
        minutes = int(minutes or 0)
        hours = int(hours)

        date = datetime(year=now.year, month=now.month, day=now.day,
                        hour=hours, minute=minutes)

        if now.hour > 15:
            date += timedelta(days=1)

        return date


assert parse_hour("9H30", now=datetime(year=1984, month=1, day=10, hour=6))\
                 == datetime(year=1984, month=1, day=10, hour=9, minute=30)
assert parse_hour("8h", now=datetime(year=1984, month=1, day=10, hour=18))\
                 == datetime(year=1984, month=1, day=11, hour=8, minute=00)


def time_to_int(string: str, identifiant: int):
    '''Parse and substract the hour'''
    date = parse_hour(string)
    d = USERS[identifiant]["distance"]
    date -= timedelta(minutes=d)

    response = date.strftime('%HH%M')
    return response


def belong(list: list, x: int):
    if len(list) == 0:
        return False
    for i in range(len(list)):
        if list[i] == x:
            return True
    return False


def message(list: list, string: str) -> str:
    '''Create the final recap message.'''
    msg = "Liste des participants pour " + str(string) + " : \n"
    if len(list) == 0:
        return "Il n'y a pas de participant"
    for i in range(len(list)):
        id = list[i]
        t = time_to_int(string, id)
        msg = msg + "<@" + str(id) + "> doit partir à **" + str(t) + "**\n"

    return msg
