from time import time, gmtime, mktime

def convert_unix(output_format, input_time=None):
    if input_time is None:
        input_time = time()
    
    if output_format == "HH:MM" or output_format == "clock":
        return "{:02d}:{:02d}".format(gmtime(input_time)[3], gmtime(input_time)[4])
    elif output_format == "HH:MM:SS" or output_format == "time":
        return "{:02d}:{:02d}:{:02d}".format(gmtime(input_time)[3], gmtime(input_time)[4], gmtime(input_time)[5])
    elif output_format == "DD.MM.YYYY" or output_format == "date":
        return "{:02d}.{:02d}.{:04d}".format(gmtime(input_time)[2], gmtime(input_time)[1], gmtime(input_time)[0] % 100)
    elif output_format == "rounded":
        h, m = gmtime(input_time)[3:5]
        return f"{m}m" if h == 0 else f"{h + (m >= 45)}h" if m < 15 or m >= 45 else f"{h},5h"
    elif output_format == "datetime":
        year, month, day, hour, minute, _, _, _ = time.localtime(input_time)
        return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}".format(year, month, day, hour, minute)
    elif output_format == "rtc":
        year, month, day, _, hour, minute, _, _ = time.localtime(input_time)
        return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}".format(year, month, day, hour, minute)
    elif output_format == "weekday":
        return gmtime(input_time)[6]
    elif output_format == "leap":
        return isLeapYear(input_time)
    elif output_format == "date_manual":
        return timeToDate(input_time)
        
    else:
        return input_time

def convert_datetime(output_format, input_time):
    date_part, time_part = input_time.split('T')
    year, month, day     = map(int, date_part.split('-'))
    hour, minute         = map(int, time_part.split(':'))
    if output_format == "unix":
        tm = (year, month, day, hour, minute, -1, -1, -1)
        return mktime(tm)
    elif output_format == "rtc":
        tm = (year, month, day, -1, hour, minute, 0, 0)
        return tm
    elif output_format == "HH:MM" or output_format == "clock":
        return "{:02d}:{:02d}".format(hour, minute)
    elif output_format == "HH:MM:SS":
        return "{:02d}:{:02d}:{:02d}".format(hour, minute, 0)
    elif output_format == "DD.MM.YYYY" or output_format == "date":
        return "{:02d}.{:02d}.{:04d}".format(day, month, year % 100)
    else:
        return input_time

def isLeapYear(t = time()):
    y = gmtime(t)[0]
    if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
        return True
    else:
        return False

def timeToDate(unix_timestamp=time()):
    # Definiere die Anzahl der Tage in jedem Monat
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # Startdatum: 1. Januar 1970
    year = 1970
    month = 1
    day = 1

    # Füge die Tage des Zeitstempels hinzu
    day += unix_timestamp // (24 * 3600)

    # Berechne das aktuelle Jahr
    while True:
        leap = 1 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 0
        days_in_year = 365 + leap
        if day > days_in_year:
            day -= days_in_year
            year += 1
        else:
            break

    # Berechne den aktuellen Monat
    for i in range(12):
        days_in_month = 29 if i == 1 and leap else month_days[i]
        if day > days_in_month:
            day -= days_in_month
            month += 1
        else:
            break

    return "{:02d}.{:02d}.{:04d}".format(day, month, year)
