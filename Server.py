import usocket
import time
import network
import gc
from pyb import LED

led = LED(3) # 1=red, 2=green, 3=blue

def web_page(input_values=[]):
    f = open('code.html','r')
    html = f.read()
    f.close()
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
    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM,usocket.SO_REUSEADDR)
    socket.bind(('', 80))
    socket.listen(5)
    while True:
      try:
        if gc.mem_free() < 102000:gc.collect()
        conn, addr = socket.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        #print('Content = %s' % request)
        
        ## PARSE REQUEST
        print(request)
        
        data_index = request.find('/?data') == 6
        http_index = request.find('HTTP')
        date_time = request[data_index+12:http_index]
        date_time = date_time.replace('%20', ' ')
        print('time', date_time)
                
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
      except OSError as e:
        conn.close()
        print('Connection closed', e)


access_point = create_access_point()
serve(access_point)