import pyb
import utime
import settings
from array import array
import time



def position(pw, wait_time=2):
    servo_pin = pyb.Pin(settings.servo_pin, pyb.Pin.OUT_PP)
    utime.sleep_ms(10)
    start_counter = utime.ticks_ms()
    while True:
        servo_pin.high()
        utime.sleep_us(pw)
        servo_pin.low()
        utime.sleep_ms(20)
        current_counter = utime.ticks_ms()
        if current_counter - start_counter > (wait_time * 1000): break
        
        
if __name__ == "__main__":
    position(1500)
    position(1000)
    position(2000)