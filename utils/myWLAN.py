""" __init__.py """
# from .myWLAN import WLANManager
# from .config import WLANConfig   #eigentlich nicht notwendig
 
""" config.py """
# class WLANConfig:
# 
#     def __init__(self, ssid, pw, ip=None):
#         self.ssid = ssid
#         self.pw = pw
#         self.ip = ip
# 
# wlan_list = [
#     WLANConfig("ssid0", "pw0"),    #0
#     WLANConfig("ssid1", "pw1"),    #1
#     WLANConfig("ssid2", "pw2")  #2
# ]
# 
# WLAN_DEFAULT = 1
 
""" Beispielverwendung """
#     from utils import WLANManager
#     wlanManager = WLANManager()
#     try:
#         ip = wlanManager.connect(wlan_index=1)  # Verbindet sich mit dem WLAN an Index 1
#         print(f"Verbunden mit IP: {ip}")
#     except KeyboardInterrupt:
#         pass
 
# oder
 
#     from utils import WLANManager
#     wlan = WLANManager()
#     ip = wlan.connect()
 
import network
import socket
import time
import utils.myWLAN_config as config
 
class WLANManager:
    
    def addWLAN(self, ssid, pw, ip=None, set_as_default=False):
        config.wlan_list.append(config.WLANConfig(ssid, pw, ip))
        if set_as_default:
            self.setDefault(len(config.wlan_list) - 1)
 
    @staticmethod
    def setDefault(i):
        if 0 <= i < len(config.wlan_list):
            config.WLAN_DEFAULT = i
        else:
            raise ValueError("Index außerhalb des Bereichs")
 
    def setSSID(self, ssid, i=config.WLAN_DEFAULT):
        config.wlan_list[i].ssid = ssid
        
    def setPW(self, pw, i=config.WLAN_DEFAULT):
        config.wlan_list[i].pw = pw
 
    def setIP(self, ip, i=config.WLAN_DEFAULT):
        config.wlan_list[i].ip = ip
 
    @staticmethod
    def getDefault():
        return config.WLAN_DEFAULT
 
    def getSSID(self, i=config.WLAN_DEFAULT):
        return config.wlan_list[i].ssid
 
    def getPW(self, i=config.WLAN_DEFAULT):
        return config.wlan_list[i].pw
 
    def getIP(self, i=config.WLAN_DEFAULT):
        return config.wlan_list[i].ip
    
class WLAN:
    
    sta    = None
    sta_if = None
    ap     = None
    ap_if  = None
    
    @classmethod
    def connect(cls, ssid=None, pw=None, wlan_index=None, set_as_default=False, max_attempts=10):
        def attempt_connection(ssid, pw):
            cls.sta = network.WLAN(network.STA_IF)
            cls.sta.active(True)
            print('Connecting to', ssid, sep=" ")
            cls.sta.connect(ssid, pw)
            for _ in range(max_attempts):
                if cls.sta.isconnected():
                    return cls.sta.ifconfig()[0]
                print('Waiting for connection...')
                time.sleep(1)
            cls.sta.active(False)
            return None
 
        if wlan_index is not None and 0 <= wlan_index < len(config.wlan_list):
            wlan_config = config.wlan_list[wlan_index]
            ip = attempt_connection(wlan_config.ssid, wlan_config.pw)
            if ip:
                return ip
            # Falls die Verbindung fehlschlägt, versuche es mit der nächsten Konfiguration
        for wlan_config in config.wlan_list:
            ip = attempt_connection(wlan_config.ssid, wlan_config.pw)
            if ip:
                return ip
        raise ValueError("Keine WLAN-Verbindung möglich")
 
    @classmethod
    def createAP(cls):
        cls.ap = network.WLAN(network.AP_IF)
        cls.ap.config(ssid='PiPico', password='password')
        cls.ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
        cls.ap.active(True)
 
        # wait for wifi to go active
        wait_counter = 0
        while cls.ap.active() == False:
            print("waiting " + str(wait_counter))
            time.sleep(0.5)
            pass
 
        print('WiFi active')
        cls.ap_if = cls.ap.ifconfig()
        print(cls.ap_if)
        print('Pico SSID = ' + cls.ap.config("ssid"))
        print('IP address = ' + cls.ap_if[0])
        print('subnet mask = ' + cls.ap_if[1])
        print('gateway  = ' + cls.ap_if[2])
        print('DNS server = ' + cls.ap_if[3])
 
        ip = cls.ap_if[0]
        addr = (ip, 80)
        cls.ap = socket.socket()
        cls.ap.bind(addr)
        cls.ap.listen(1)
        print('listening on', addr)
        print (cls.ap)
 
    @classmethod
    def checkAPRequest(cls):
        while True:
            client, client_addr = cls.ap.accept()
            raw_request = client.recv(1024)
            raw_request = raw_request.decode("utf-8")
            print(raw_request)
            return raw_request
    
    
 
if __name__ == "__main__":
    try:
        ip = WLAN.connect()
    except:
        WLAN.createAP()
        WLAN.checkAPRequest()