from ..core.enums import severityType
from datetime import datetime


def log(msg, severity=severityType.Message):
    if not type(msg) == str:
        raise TypeError('Message is of wrong type.')
    print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] - [{severity}] -> {msg}')
