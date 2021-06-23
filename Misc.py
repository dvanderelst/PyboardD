import Settings
import time

def boot_display():
    red = Settings.red
    green = Settings.green
    blue = Settings.blue
    leds = [red, green, blue]
    for x in range(3):
        for led in leds:
            led.on()
            time.sleep(0.5)
            led.off()
    red.off()
    green.off()
    blue.off()
    

def connect_received_display():
    blue = Settings.blue
    blue.off()
    blue.on()
    time.sleep(0.25)
    blue.off()
    
    
    


def lst2str(lst):
    if isinstance(lst, str): return lst
    text = ''
    for x in lst: text += str(x) + ' '
    text = text.rstrip(' ')
    return text
