from machine import Pin

class Key:
    def __init__(self, key, pin):
        self.key = key
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.state = False
        self.last_state = False

    def get_state(self):
        if self.pin.value() == 0:
            if self.state == False:
                self.state = True
                return True
            else:
                return False
        else:
            self.state = False
            return False
    
    def action(self):
        if self.key == 0:
            print("key0")
        elif self.key == 1:
            print("key1")
        elif self.key == 2:
            print("key2")


if __name__ == "__main__":
    from time import sleep_ms

    keys = [Key(0, pin=2), Key(1, pin=3), Key(2, pin=15)]

    while True:
        for key in keys:
            if key.get_state():
                key.action()
            else:
                pass
        sleep_ms(50)
