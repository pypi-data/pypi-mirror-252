import datetime
from collections.abc import Iterable
from decimal import Decimal as D


def normalize(data):

    if isinstance(data, dict):
        result = {}
        for key, val in data.items():
            result[key] = normalize(val)
        return result

    if isinstance(data, Iterable):
        result = []
        for item in data:
            result.append(normalize(item))
        return result

    if isinstance(data, D):
        return float(data)

    if isinstance(data, datetime.datetime):
        return data.timestamp()

    if type(data) in (bool, int, float):
        return data

    return str(data)