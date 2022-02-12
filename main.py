########################################################################################
# FOR BME SCANNER
########################################################################################

import settings
import gc
import misc
import ujson
import measure
import server
import time

green = settings.green
blue = settings.blue
red = settings.red

gc.collect()
misc.boot_display_field()
green.off()
red.off()
blue.off()

server.create_access_point(essid = settings.essid)


while True:
    free_mem = gc.mem_free()
    print('Free memory:', free_mem)
    data_server = server.Server()
    message = data_server.receive_data()
    print('Rcvd message:', message)
    message = message.split(settings.data_sep)
    sample_rate = int(message[0])
    duration = int(message[1])
    green.off()
    blue.on()    
    buffer = measure.measure(1, sample_rate, duration)
    print('Measurement completed', len(buffer))
    blue.off()
    buffer = ujson.dumps(buffer)
    data_server.send_data(buffer)
    time.sleep(0.5)
    del(data_server)
    del(buffer)
    gc.collect()
   
