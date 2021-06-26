import settings
import time


def lst2txt(lst, sep=','):
    txt = ''
    for x in lst: txt = txt + str(x) + sep
    txt = txt.rstrip(sep)
    return txt

def boot_display():
    red = settings.red
    green = settings.green
    blue = settings.blue
    leds = [red, green, blue]
    for x in range(3):
        for led in leds:
            led.on()
            time.sleep(0.1)
            led.off()
    red.off()
    green.off()
    blue.off()
    

def connect_received_display():
    blue = settings.blue
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
