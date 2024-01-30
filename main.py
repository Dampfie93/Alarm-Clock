from dfplayer import *
from eink2in9 import *
from RC522      import *
from utils      import *
from alarm_manager import Alarm

from time import sleep, time, gmtime, mktime
import machine
import _thread
UART_INSTANCE=0
TX_PIN = 16
RX_PIN=17
BUSY_PIN=6
led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
display = Display()
player = DFPlayer(uartInstance=0, txPin=16, rxPin=17, busyPin=20)
keys = [Key(0, pin=2), Key(1, pin=3), Key(2, pin=15)]

WAIT_FOR_RFID = False
PLAY_SOUND = False

def init():
    alarm_list_init = [
        # Alarm(True, time()+20,  0),
        # Alarm(True, time()+7200, 1, "1111111")
    ]

    Alarm.setAlarmListtoJson(alarm_list_init)
    Alarm.getAlarmListfromJson()


    log ("DEBUG",  f"ALARMS: {len(Alarm.alarm_list)}")
    log ("DEBUG",  f"RFIDS: {len(RFIDManager.rfids)}")
    log ("DEBUG", f"{dateStr()}")
    display.show("hello", True)
    try:
        ip = WLAN.connect()
        setTimeAPI()
        print(gmtime()[3],":",gmtime()[4],":",gmtime()[5])
    except:
        pass
    display.show("time", False)

def main():     
    restart=True
    while restart:
        restart = False
        display.show("time", False) if not display.checkTime() and display.active_screen == "time" else None
        #check Alarm List
        for alarm in Alarm.alarm_list:
            #remove unneeded past Alarm (return None)
            if alarm.check() is None: # type: ignore
                Alarm.alarm_list.remove(alarm) # type: ignore
                Alarm.to_json(Alarm.alarm_list)
                log("ALARM", "Snooze deleted")
                break
            elif alarm.check(): # type: ignore
                log("ALARM", f"activated")
                alarm.setNextTrigger() # type: ignore
                display.show("alarm", True)
                WAIT_FOR_RFID = True
                PLAY_SOUND = True
            if WAIT_FOR_RFID:
                RFIDReader.power(True)
                print(f"[{timeStr(time())}] [ALARM] wartet auf rfid")
                if RFIDManager.check():
                    log("ALARM", f"disarmed")
                    RFIDReader.power(False)
                    WAIT_FOR_RFID= False
                    PLAY_SOUND = False
                    display.show("alarm_off", True)
                    display.show("time", False)
        sleep(0.25)
        blinkLED()
        restart = True

def blinkLED():
    if time() % 2 == 0:
        led_onboard.on()
    else:
        led_onboard.off()

if __name__ == "__main__":
    init()
    main()
    # _thread.start_new_thread(main, ())