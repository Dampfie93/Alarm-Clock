# import urequests
import socket
from   machine import RTC, Pin
from   utils   import WLANManager

import network
import time

ssid = 'PiPico'
password = 'password'

ap = network.WLAN(network.AP_IF)
ap.config(ssid=ssid, password=password)
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
ap.active(True)

# wait for wifi to go active
wait_counter = 0
while ap.active() == False:
    print("waiting " + str(wait_counter))
    time.sleep(0.5)
    pass

print('WiFi active')
status = ap.ifconfig()
print('Pico SSID = ' + ap.config("ssid"))
print('IP address = ' + status[0])
print('subnet mask = ' + status[1])
print('gateway  = ' + status[2])
print('DNS server = ' + status[3])

ip = status[0]
addr = (ip, 80)
s = socket.socket()
s.bind(addr)
s.listen(1)
print(s)
print('listening on', addr)


led = machine.Pin('LED', machine.Pin.OUT, value=0)

led_state = False


while True:
    client, client_addr = s.accept()
    raw_request = client.recv(1024)
    raw_request = raw_request.decode("utf-8")
    print(raw_request)
    
    request_parts = raw_request.split()
    http_method   = request_parts[0]
    request_url   = request_parts[1]
    
    if request_url.find("/ledon") != -1:
        led_state = True
        led.on()
        print("AN")
    elif request_url.find("/ledoff") != -1:
        led_state = False
        led.off()
        print("AUS")
    else:
        pass
    
    led_state_text = "OFF"
    if led_state:
        led_state_text = "ON"
        
    file = open("led.html")
    html = file.read()
    file.close()
    
    html = html.replace("**ledState**", led_state_text)
    client.send(html)
    client.close()

