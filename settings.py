import pyb

red = pyb.LED(1)
green = pyb.LED(2)
blue = pyb.LED(3)

adc_pin = 'X8'
trigger_pin = 'X1'
signal_threshold = 2000
sample_rate = 20000
duration = 25

servo_pin = 'X6'
servo_pulse_range = [900, 2100] # in usecs


