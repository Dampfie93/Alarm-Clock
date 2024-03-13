from time import sleep, sleep_ms, time, gmtime, mktime, localtime
from utils import FileManager, log, convert_unix, convert_datetime


class Alarm(FileManager):
    
    alarm_list = []

    def __init__(self, active, time, repeat, weekday="1111111", snooze=None, snoozetime=None, sound=None, rfid=None):
        self.active     = active
        self.time       = time
        self.repeat     = repeat
        self.weekday    = weekday
        self.snooze     = snooze
        self.snoozetime = snoozetime
        self.sound      = sound
        self.rfid       = rfid

    def __str__(self):
        attributes_order = [
            self.active,
            self.time,
            self.repeat,
            self.weekday,
            self.snooze,
            self.snoozetime,
            self.sound,
            self.rfid
        ]
        return ', '.join([f"{value}" for value in attributes_order])

    @classmethod
    def isAlarmActiveInList(cls):
        for alarm in cls.alarm_list:
            if alarm.checkAlarm() is False:
                return False
            elif alarm.checkAlarm() is None:
                cls.alarm_list.remove(alarm) # type: ignore
                cls.to_json(Alarm.alarm_list)
                log("ALARM", "Snooze deleted")
                return False
            elif alarm.checkAlarm():
                alarm.setNextTrigger() # type: ignore
                log("ALARM", f"activated")
                return True
        return False


    def checkAlarm(self):
        if self.repeat == -1 and not self.active:
            return None

        checkActive  = self.active == True
        checkTime    = self.time <= time() and self.time+120 >= time()
        alarmTrigger = checkActive and checkTime
        return alarmTrigger
        
    def setNextTrigger(self):
        self.active = False if self.repeat == 0 or self.repeat == -1 else self.active
        if self.repeat == 1:
            for i in range(1, 8):
                nextDay = (gmtime()[6] + i) % 7
                if self.weekday[nextDay] =="1":
                    self.time +=i*24*3600
                    #self.time +=20
                    log("ALARM", f"next: {convert_unix.date(self.time)} at {convert_unix.time(self.time)}")
                    break
        Alarm.setAlarmListtoJson()
    
    @staticmethod
    def _nextActiveDay(current_wday, weekday_str):
        """
        Determine the next active day after the current weekday, based on the weekday string.
        """
        for i in range(1, 8):  # Start from the next day (i = 1)
            next_wday = (current_wday + i) % 7
            if weekday_str[next_wday] == '1':
                return i  # Number of days to add to current day
        return None  # No active days found

    @classmethod
    def addAlarm(cls, hour, minute, repeat, weekday):
        # Adjusting for timezone
        timezone = 0
        utc_offset_seconds = timezone * 3600  # Convert hours to seconds

        # Current time in local timezone
        now = localtime(time() + utc_offset_seconds)
        alarm_time = mktime((now[0], now[1], now[2], hour, minute, 0, now[6], now[7]))

        # Check if today
        if weekday[now[6]] == '1' and alarm_time > time() + utc_offset_seconds:
            pass  # Alarm is set for today
        else:
            # Find the next active day
            days_to_add = cls._nextActiveDay(now[6], weekday)
            if days_to_add is not None:
                alarm_time += days_to_add * 86400  # Add the necessary days in seconds
        
        # Adjusting alarm time back to UTC
        alarm_time -= utc_offset_seconds

        # Create and add the new alarm
        new_alarm = cls(True, alarm_time, repeat, weekday)
        cls.alarm_list.append(new_alarm)
        print(f"Added alarm: {new_alarm}")

        # Update alarm list
        cls.setAlarmListtoJson()
        return alarm_time, repeat, weekday

    @classmethod
    def getNextAlarm(cls):
        next_alarm = None
        next_alarm_t = time()+86400  # day in seconds
        for i, alarm in enumerate(cls.alarm_list):
            checkActive = alarm.active # type: ignore
            checkTime   = alarm.time > time() # type: ignore
            checkNext   = alarm.time < next_alarm_t # type: ignore
            if checkActive and checkTime and checkNext:
                next_alarm    = i
                next_alarm_t  = alarm.time # type: ignore
        return next_alarm
    
    @classmethod
    def getAlarmListfromJson(cls):
        cls.alarm_list = cls.from_json()
        return cls.alarm_list
    
    @classmethod
    def setAlarmListtoJson(cls, alarm_list = None):
        if alarm_list is None:
            alarm_list = cls.alarm_list
        cls.to_json(alarm_list)