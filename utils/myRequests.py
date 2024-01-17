import urequests
import machine
import socket


def setTimeAPI():
    response = urequests.get('https://timeapi.io/api/Time/current/zone?timeZone=Europe/Berlin')
    r = response.json()
    t = (r['year'], r['month'], r['day'], r['dayOfWeek'], r['hour'], r['minute'], r['seconds'], r['milliSeconds'])
    machine.RTC().datetime(t)
    print(machine.RTC().datetime())
    
def getWeather():
    response = urequests.get('https://api.brightsky.dev/current_weather?lat=50.078217&lon=8.239761')
    r = response.json()['weather']
    print(r['condition'],r['temperature'], r['icon'])




if __name__ == "__main__":
    from utils import WLAN
    ip = WLAN.connect()
    print(ip)
    getWeather()
    
