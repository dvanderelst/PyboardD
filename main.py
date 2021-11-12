########################################################################################
# FOR BME SCANNER
########################################################################################

import settings
import time
import gc
import misc
import ujson
import measure
import servo
import server
import sys
import os

green = settings.green
blue = settings.blue
red = settings.red

gc.collect()
misc.boot_display_field()
server.create_access_point(essid = settings.essid)

while True:
    green.on()
    data_server = server.Server()
    message = data_server.receive_data()
    print(message)
    message = message.split(settings.data_sep)
    sample_rate = int(message[0])
    duration = int(message[1])
    green.off()
    blue.on()
    buffer = measure.measure(1, sample_rate, duration)
    blue.off()

    buffer = ujson.dumps(buffer)
    data_server.send_data(buffer)
    del(data_server)
    gc.collect()

