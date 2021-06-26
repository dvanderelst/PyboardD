import utime
import pyb
import array
import pyb
import json
import time
import machine
import settings
import misc

adc1 = pyb.ADC(pyb.Pin.board.X8)
trigger_pin1 = pyb.Pin('X1', pyb.Pin.OUT_PP)

adc2 = pyb.ADC(pyb.Pin.board.Y12)
trigger_pin2 = pyb.Pin('X2', pyb.Pin.OUT_PP)

trigger_pin1.low()
trigger_pin2.low()


def measure(channel, fs, duration):
    value = 0
    signal_threshold = settings.signal_threshold
    samples = int((fs/1000) * duration)
    timer = pyb.Timer(6, freq=fs)
    buffer = array.array('H', (0 for i in range(samples)))
    
    if channel == 1: trigger_pin1.high()
    if channel == 2: trigger_pin2.high()
    
    utime.sleep_us(50)
    
    trigger_pin1.low()
    trigger_pin2.low()
    
    start_counter = utime.ticks_ms()
    while value < signal_threshold:
        if channel == 1: value = adc1.read()
        if channel == 2: value = adc2.read()
        current_counter = utime.ticks_ms()
        if current_counter - start_counter > 100: break

    
    if channel == 1: adc1.read_timed(buffer, timer)
    if channel == 2: adc2.read_timed(buffer, timer) 
    
    return buffer


def measure_both(first, second, fs, duration):
    buffer1 = measure(first, fs, duration)
    utime.sleep_ms(100)
    buffer2 = measure(second, fs, duration)
    total = buffer1 + buffer2
    return total


def write_data(buffer, file_name, prefixes = [], mode='a', sep=','):
    f = open(file_name, mode)
    for x in buffer:
        line = prefixes + [x]
        line = misc.lst2txt(line, sep=sep)
        f.write(line + '\n')
    f.close()
    
    



if __name__ == "__main__":
    for x in range(3):
        trigger_pin1.low()
        trigger_pin2.low()
        time.sleep(3)
        trigger_pin1.high()
        trigger_pin2.high()
        time.sleep(3)
    for x in range(5):
        result = measure(1, 10000, 30)
        time.sleep(1)
    for x in result: print(x)
        
        

        
