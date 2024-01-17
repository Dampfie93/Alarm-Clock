# import urequests
import socket
from   machine import RTC, Pin
from   utils   import WLANManager

def openPort(ip=None):
    ip = WLANManager.getIP() if ip is None else ip
    addr = (ip, 80)
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
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


if __name__ == "__main__":
    wlan = WLANManager()
    ip = wlan.connect()

    openPort(ip)