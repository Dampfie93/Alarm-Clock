from dfplayer import *
from eink2in9 import *
from rc522      import *
from utils      import *
from webserver  import *
from alarm_manager import Alarm
# from webserver.phew import logging
# logging.set_truncate_thresholds(11 * 1024, 8 * 1024)
# logging.info("Info")
# logging.warn("Warn")
# logging.error("Error")
# logging.debug("Debug")
# logging.exception("Exception")
from time import sleep, time
import machine  #type: ignore
import _thread

led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
display = Display()
player = DFPlayer(uartInstance=0, txPin=16, rxPin=17, busyPin=20)
keys = [Key(0, pin=2), Key(1, pin=3), Key(2, pin=15)]

MAIN_STATE = None

def testAlarmList():
    alarm_list_init = [
        # Alarm(True, time()+20,  0),
        # Alarm(True, time()+7200, 1, "1111111")
    ]
    Alarm.setAlarmListtoJson(alarm_list_init)

def init():
    Alarm.getAlarmListfromJson()
    logging.info(f"[INIT] ALARMS: {len(Alarm.alarm_list)}")
    logging.info(f"[INIT] RFIDS:  {len(RFIDManager.rfids)}")

    display.show("hello", True)
    state("time")

def state(state=None):
    global MAIN_STATE

    if state is None:
        return MAIN_STATE
    
    if state == "alarm":
        display.show("alarm", True)
        logging.info("Alarm activated!")

    elif state == "alarm_off":
        display.show("alarm_off", True)
        logging.info("Alarm disarmed!")

    elif state == "time":
        display.show("time", False)

    MAIN_STATE = state
    logging.debug(f"Main-State: {state}")


def main():     
    restart=True
    while restart:
        restart = False
        if time() % 3600 == 0: # every hour
            setTimeAPI()
        if time() % 60 == 0: # every minute
            Alarm.getAlarmListfromJson()
        # Check if alarm is active
        if state() != "alarm":
            if Alarm.isAlarmActiveInList():
                state("alarm")
        
        # Check if key is pressed
                
        # Update Time
        if state() == "time":
            display.updateTime()

        # Alarm State
        elif state() == "alarm":
            logging.debug("waiting for RFID")
            if RFIDManager.isCardFound():
                state("alarm_off")
                state("time")
        sleep(0.25)
        blinkLED()
        restart = True


def blinkLED():
    if time() % 2 == 0:
        led_onboard.on()
    else:
        led_onboard.off()


if __name__ == "__main__":
    if not connect_wifi():
        logging.error("No connection to Wifi!")
        logging.debug("Access Point started!")
        core1 = _thread.start_new_thread(start, ("ap", ))
    else:
        setTimeAPI()
        logging.debug("Connected to Wifi!")
        logging.debug("Starting Webserver!")
        core1 = _thread.start_new_thread(start, ("sta", ))
    init()
    main()