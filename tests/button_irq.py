from machine import Pin
from time import sleep

button = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(3, Pin.IN, Pin.PULL_UP)
button3 = Pin(15, Pin.IN, Pin.PULL_UP)
led = Pin('LED', Pin.OUT, value=0)

def button_handler(pin):
    print(pin[])
    print(len(str(pin)))
#     if pin[0] == "GPIO2":
#         led.on() if pin[2]=="PULL_UP" else led.off()
# 
while True:
    # Beim Drrücken des Buttons, GPIO="high"
    # Pin(GPIO2, mode=IN, pull=PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)
    sleep(0,5)