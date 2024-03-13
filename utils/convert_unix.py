from time import gmtime, localtime, time

def _get_input_time(input_time=None):
    return input_time if input_time is not None else time()

def clock(input_time=None):
    input_time = _get_input_time(input_time)
    return "{:02d}:{:02d}".format(gmtime(input_time)[3], gmtime(input_time)[4])

def time(input_time=None):
    input_time = _get_input_time(input_time)
    return "{:02d}:{:02d}:{:02d}".format(gmtime(input_time)[3], gmtime(input_time)[4], gmtime(input_time)[5])

def date(input_time=None):
    input_time = _get_input_time(input_time)
    return "{:02d}.{:02d}.{:04d}".format(gmtime(input_time)[2], gmtime(input_time)[1], gmtime(input_time)[0])

def rounded(input_time=None):
    input_time = _get_input_time(input_time)
    h, m = gmtime(input_time)[3:5]
    return f"{m}m" if h == 0 else f"{h + (m >= 45)}h" if m < 15 or m >= 45 else f"{h},5h"

def datetime(input_time=None):
    input_time = _get_input_time(input_time)
    year, month, day, hour, minute, _, _, _ = localtime(input_time)
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}".format(year, month, day, hour, minute)

def rtc(input_time=None):
    input_time = _get_input_time(input_time)
    year, month, day, _, hour, minute, _, _ = localtime(input_time)
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}".format(year, month, day, hour, minute)

def weekday(input_time=None):
    input_time = _get_input_time(input_time)
    return gmtime(input_time)[6]

def leapyear(input_time=None):
    input_time = _get_input_time(input_time)
    year = gmtime(input_time)[0]
    is_leapyear = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    return is_leapyear