from .mfrc522 import MFRC522
from machine import Pin
            
reader = MFRC522(spi_id=0,sck=18,miso=4,mosi=19,cs=5,rst=22)
pwr_rfid = Pin(26, Pin.OUT, value=0)

class RFIDReader():
    @staticmethod
    def read():
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        #print('request stat:',stat,' tag_type:',tag_type)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                return int.from_bytes(bytes(uid),"little",False) # type: ignore
            else:
                return False
        else:
            return False
        
    @staticmethod
    def power(state):
        if state is None or "off":
            pwr_rfid.off()
        else:
            pwr_rfid.on()
            
class RFIDManager():

    rfids = [
        ("Keychain", 2776760755),
        ("Card Blank", 2905187011),
        ("Mattiaqua", 230833895),
        ("McFit", 1388548041),
        ("Sticker Window", 36432398500168708),
        ("Sticker", 37276823415002884),
        ("Sticker", 36150923522136580),
        ("Sticker", 36150923524818692)]
    
#     def __init__(self, description, code):
#         self.description  = description
#         self.code         = code
    
    @classmethod
    def check(cls):
        card = RFIDReader.read()
        for rfid in cls.rfids:
            if rfid[1] == card:
                return True
