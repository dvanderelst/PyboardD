import utime
import pyb
import array
import pyb
import json
import time
import machine
import settings
import misc

adc_pin = pyb.ADC(settings.adc_pin)
trigger_pin = pyb.Pin(settings.trigger_pin, pyb.Pin.OUT_PP)
trigger_pin.low()


def measure(fs, duration):
    value = 0
    signal_threshold = settings.signal_threshold
    samples = int((fs/1000) * duration)
    timer = pyb.Timer(6, freq=fs)
    buffer = array.array('H', (0 for i in range(samples)))
    trigger_pin.high()
    utime.sleep_us(30)    
    trigger_pin.low()
    start_counter = utime.ticks_ms()
    while value < signal_threshold:
        value = adc_pin.read()
        current_counter = utime.ticks_ms()
        if current_counter - start_counter > 100: break
    adc_pin.read_timed(buffer, timer)
    return buffer


def write_data(buffer, file_name, prefixes = [], mode='a', sep=','):
    f = open(file_name, mode)
    buffer_text = misc.lst2txt(buffer, sep=sep)
    prefix_text = misc.lst2txt(prefixes, sep=sep)
    total_text = prefix_text + sep + buffer_text
    f.write(total_text + '\n')
    f.close()
    



if __name__ == "__main__":
    measure(10000,10)
        

        
