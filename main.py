import settings

#field or robot
context = 'robot'

green = settings.green
blue = settings.blue
red = settings.red

########################################################################################
# FIELD CONTEXT
########################################################################################
if context == 'field':
    import time
    import gc
    import misc
    import ujson
    import measure
    import servo
    import server
    import sys
    import os
    import pyb
    
    gc.collect()
    misc.boot_display_field()
    server.create_access_point()
    current_servo_position = -10000
    
    while True:
        green.on()
        data_server = server.Server()
        
        message = data_server.receive_data()
        print(message)
        message = message.split(settings.data_sep)
        servo_position = int(message[0])
        sample_rate = int(message[1])
        duration = int(message[2])
        
        green.off()
        blue.on()
        if current_servo_position != servo_position:
            servo.position(servo_position)
            current_servo_position = servo_position
        buffer = measure.measure(1, sample_rate, duration)
        blue.off()

        buffer = ujson.dumps(buffer)
        data_server.send_data(buffer)
        
        data_server.disconnect()
        del(data_server)
        gc.collect()


########################################################################################
# ROBOT CONTEXT
########################################################################################

if context == 'robot':
    import usocket
    import time
    import gc
    import misc
    import measure
    import server
    import ujson
        
    green = settings.green
    blue = settings.blue
    red = settings.red

    gc.collect()
    misc.boot_display_robot()
    
    green.on()
    red.on()
    server.connect2wifi()
    time.sleep(1)
    green.off()
    red.off()
    while True:
        green.on()
        data_server = server.Server()
        
        message = data_server.receive_data()
        message = message.split(settings.data_sep)
        first = int(message[0])
        second = int(message[1])
        sample_rate = int(message[2])
        duration = int(message[3])
        
        green.off()
        blue.on()
        buffer = measure.measure_both(first, second, sample_rate, duration)
        blue.off()

        buffer = ujson.dumps(buffer)
        data_server.send_data(buffer)
        
        data_server.disconnect()
        del(data_server)
        gc.collect()
        
        
        
        
        
        
        
        
        
        