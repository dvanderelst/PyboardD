import utime
import pyb
import array
import pyb
import json
import time
import machine
import settings
import misc

adc_pin1 = pyb.ADC(settings.adc_pin1)
trigger_pin1 = pyb.Pin(settings.trigger_pin1, pyb.Pin.OUT_PP)
trigger_pin1.low()

adc_pin2 = pyb.ADC(settings.adc_pin2)
trigger_pin2 = pyb.Pin(settings.trigger_pin2, pyb.Pin.OUT_PP)
trigger_pin2.low()
        

def measure(channel, fs, duration):
    value = 0
    samples = int((fs/1000) * duration)
    timer = pyb.Timer(6, freq=fs)
    buffer = array.array('H', (0 for i in range(samples)))
    
    if channel == 1: trigger_pin1.high()
    if channel == 2: trigger_pin2.high()
    
    utime.sleep_us(50)
    
    trigger_pin1.low()
    trigger_pin2.low()
    signal_threshold = settings.signal_threshold
    start_counter = utime.ticks_ms()
    while value < signal_threshold: #The sensor takes actually quite a while (tens of ms) to start emitting
        if channel == 1: value = adc_pin1.read()
        if channel == 2: value = adc_pin2.read()
        current_counter = utime.ticks_ms()
        if current_counter - start_counter > 100: break
    if channel == 1: adc_pin1.read_timed(buffer, timer)
    if channel == 2: adc_pin2.read_timed(buffer, timer)
    return buffer


def write_data(buffer, file_name, prefixes = [], mode='a', sep=','):
    f = open(file_name, mode)
    buffer_text = misc.lst2txt(buffer, sep=sep)
    prefix_text = misc.lst2txt(prefixes, sep=sep)
    total_text = prefix_text + sep + buffer_text
    f.write(total_text + '\n')
    f.close()
    
    
def measure_both(first, second, fs, duration):
    buffer1 = measure(first, fs, duration)
    end = utime.ticks_ms()
    utime.sleep_ms(50)
    buffer2 = measure(second, fs, duration)
    total = buffer1 + buffer2
    return total
    



if __name__ == "__main__":
    result = measure_both(1,2, 10000,20)
    #for x in result: print(x)
        

        
