from time import time, gmtime, mktime

def timeStr(t = time()):
    return "{:02d}:{:02d}:{:02d}".format(gmtime(t)[3], gmtime(t)[4], gmtime(t)[5])

def clockStr(t = time()):
    return "{:02d}:{:02d}".format(gmtime(t)[3], gmtime(t)[4])

def roundedStr(t):
    h, m = gmtime(t)[3:5]
    return f"{m}m" if h == 0 else f"{h + (m >= 45)}h" if m < 15 or m >= 45 else f"{h},5h"

def dateStr(t = time()):
    return "{:02d}.{:02d}.{:02d}".format(gmtime(t)[2], gmtime(t)[1], gmtime(t)[0] % 100)


def isLeapYear(t = time()):
    y = gmtime(t)[0]
    if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
        return True
    else:
        return False

def timeToDate(unix_timestamp=time()):
    # Made by ChatGPT
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
