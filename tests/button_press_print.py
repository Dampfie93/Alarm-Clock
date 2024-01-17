from machine import Pin
from time import sleep

KEY0 = 2
KEY1 = 3
KEY2 = 15
button = Pin(KEY0, Pin.IN, Pin.PULL_UP)
button1 = Pin(KEY1, Pin.IN, Pin.PULL_UP)
button2 = Pin(KEY2, Pin.IN, Pin.PULL_UP)

# while True:
#     if not button.value():
#         print('Button 0 pressed!')
#     elif not button1.value():
#         print('Button 1 pressed!')
#     elif not button2.value():
#         print('Button 2 pressed!')
#     sleep(0.5)

while True:
    first = button.value()
    sleep(0.01)
    second = button.value()
    if first and not second:
        print('Button pressed!')
    elif not first and second:
        print('Button released!')