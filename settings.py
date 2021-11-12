import pyb

# Common settings

red = pyb.LED(1)
green = pyb.LED(2)
blue = pyb.LED(3)

adc_pin1 = 'X7'
trigger_pin1 = 'X1'
adc_pin2 = 'X8'
trigger_pin2 = 'X2'

data_sep = ','
essid = 'otter'
signal_threshold = 2000
break_character = '*'
port_number = 1000
