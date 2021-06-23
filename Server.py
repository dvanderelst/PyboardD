import usocket
import time
import network
import gc
import Misc
from pyb import LED
import Measure
import Settings
import Plot


def web_page(input_values=[None,None]):
    f = open('code.html','r')
    html = f.read()
    f.close()
    html = html.replace('xx_time_xx',str(input_values[0]))
    html = html.replace('xx_label_xx',str(input_values[1]))
    html = html.replace('xx_graph_xx',str(input_values[2]))
    html = html.replace('xx_data_xx','')#,str(input_values[3]))
    html = html.replace('xx_file_xx',str(input_values[4]))
    return html


def create_access_point():
    access_point = network.WLAN(1)
    access_point.config(essid='PYBD')          # set AP SSID
    access_point.config(password='pybd0123')   # set AP password
    access_point.config(channel=6)             # set AP channel
    access_point.active(1)                     # enable the AP
    while access_point.isconnected() == False: pass
    print('Connection successful')
    print(access_point.ifconfig())
    return access_point


def serve(access_point):
    green = Settings.green
    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM,usocket.SO_REUSEADDR)
    socket.bind(('', 80))
    socket.listen(5)
    while True:
        green.toggle()
        try:
            
            if gc.mem_free() < 102000:gc.collect()
            conn, addr = socket.accept()
            conn.settimeout(3.0)
            Misc.connect_received_display()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            #print('Content = %s' % request)
            
            ## PARSE REQUEST
            #print(request)
            
            data_index = request.find('/?data') == 6
            end_time_index = request.find('ENDT')
            end_label_index = request.find('ENDL')
            date_time = request[data_index+12:end_time_index]
            date_time = date_time.replace('%20', ' ')
            data_label = request[end_time_index+4:end_label_index]
            
            if len(date_time)>150: date_time = ''
            if len(data_label)>50: data_label = ''
            print('data and time:', date_time)
            print('label:', data_label)
            
            total_buffer = []
            graph = ''
            output_file = ''
            if len(data_label) > 0:
                Settings.blue.on()
                output_file = data_label + "_" + date_time + '.csv'
                sample_rate = Settings.sample_rate
                duration = Settings.duration
                total_buffer = Measure.measure(1, sample_rate, duration)
                graph, min_value, max_value = Plot.plot(total_buffer)
                Settings.blue.off()
                
                    
            response = web_page([date_time, data_label, graph, total_buffer,output_file])
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except OSError as e:
            conn.close()
            print('Connection closed', e)