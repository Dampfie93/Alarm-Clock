from eink2in9.lib.EPD    import EPD
from eink2in9.lib.writer import Writer

from eink2in9.fonts import Arial72       as FONT_BIG
from eink2in9.fonts import freesans20    as FONT_MEDIUM
from eink2in9.fonts import Arial72_clock as FONT_CLOCK

from time         import sleep, time, gmtime, mktime
from utils.myTime import convert_unix, convert_datetime

class Display():
               
    def __init__(self):
        self.active_screen  = None
        self.time_h         = 0
        self.time_m         = 0
        self.top_str        = ""
        self.last_refresh   = True

    def checkTime(self):
        if self.time_h != gmtime(time())[3] or self.time_m != gmtime(time())[4]:
            return False
        else:
            return True
    
    @staticmethod
    def printClock(x_offset,y_offset):
        width = 9
        height = 8
        clock_img = [
            1,1,0,0,0,0,0,1,1,
            1,0,0,1,1,1,0,0,1,
            0,0,1,0,1,0,1,0,0,
            0,1,0,0,1,0,0,1,0,
            0,1,0,0,1,1,0,1,0,
            0,1,0,0,0,0,0,1,0,
            0,0,1,0,0,0,1,0,0,
            0,0,0,1,1,1,0,0,0]

        for y in range(height):
            for x in range(width):
                pixel_value = clock_img[y * width + x]
                if pixel_value == 1:
                    epd.pixel(x + x_offset, y + y_offset, 0x00)

    def show(self, typ, refresh):
        self.top_str = ""
        self.active_screen = typ
        print(f"Active Screen: {self.active_screen}")
        if refresh == True:
            epd.init()
            epd.fill(0xff)
        
        if typ == "time":
            self.time_h = gmtime()[3]
            self.time_m = gmtime()[4]

            wri = Writer(epd, FONT_CLOCK)
            wri.set_textpos(epd, 0, 30)
            wri.printstring(convert_unix("clock"), invert=True)
            
        elif typ == "alarm":
            wri = Writer(epd, FONT_BIG)
            wri.set_textpos(epd, 30, 30)  # verbose = False to suppress console output
            wri.printstring('ALARM', invert=True)
            
        elif typ == "alarm_off":
            wri = Writer(epd, FONT_BIG)
            wri.set_textpos(epd, 40, 30)  # verbose = False to suppress console output
            wri.printstring('OFF', invert=True)
            
        elif typ == "hello":
            epd.fill(1)
            wri = Writer(epd, FONT_BIG)
            wri.set_textpos(epd, 60, 30)  # verbose = False to suppress console output
            wri.printstring('Hallo!', invert=True)
            
        
        checkTopBar = True if typ == "time" or typ == "debug" else False
        if checkTopBar:
            epd.fill_rect(0,0,296,13, 0xff)
            if self.top_str: self.printClock(5,5)
            epd.text(self.top_str, 20, 5, 0x00)
        
        if refresh:
            epd.display_Base(epd.buffer) 
        else:
            epd.display_Partial(epd.buffer)
        self.last_refresh = refresh
        epd.sleep()
    
    def update_time(self):
        if self.checkTime() == False:
            self.show("time", False)


epd = EPD()

if __name__ == "__main__":
    display = Display("init")