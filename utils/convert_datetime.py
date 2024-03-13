from time import mktime

def _parse_input_time(input_time):
    date_part, time_part = input_time.split('T')
    year, month, day = map(int, date_part.split('-'))
    hour, minute = map(int, time_part.split(':'))
    return year, month, day, hour, minute

def unix(input_time):
    year, month, day, hour, minute = _parse_input_time(input_time)
    tm = (year, month, day, hour, minute, 0, -1, -1, -1)
    return mktime(tm)

def rtc(input_time):
    year, month, day, hour, minute = _parse_input_time(input_time)
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}"

def clock(input_time):
    _, _, _, hour, minute = _parse_input_time(input_time)
    return "{:02d}:{:02d}".format(hour, minute)

def time(input_time):
    _, _, _, hour, minute = _parse_input_time(input_time)
    return "{:02d}:{:02d}:{:02d}".format(hour, minute, 0)

def date(input_time):
    year, month, day, _, _ = _parse_input_time(input_time)
    return "{:02d}.{:02d}.{:04d}".format(day, month, year)