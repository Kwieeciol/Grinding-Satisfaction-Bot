import datetime

def date():
    return datetime.datetime.now().strftime('%d.%m.%Y')


def return_int(s: str):
    return int(''.join([l for l in s if l.isdigit()]))
