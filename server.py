import os
import socket
import sys
import time
import settings
import network


green = settings.green
blue = settings.blue
red = settings.red

#
# For use as access point in the field
#

def create_access_point(essid):
    access_point = network.WLAN(1)
    access_point.config(essid=essid)          # set AP SSID
    access_point.config(password='pybd0123')   # set AP password
    access_point.config(channel=6)             # set AP channel
    access_point.active(1)                     # enable the AP
    while access_point.isconnected() == False: pass
    print('Connection successful')
    print(access_point.ifconfig())
    return access_point


def web_page(input_values={}):
    f = open('form.html','r')
    html = f.read()
    f.close()
    if 'date_time' in input_values: html = html.replace('xx_date_time_xx', input_values['date_time'])
    if 'label' in input_values: html = html.replace('xx_label_xx', input_values['label'])
    if 'comment' in input_values: html = html.replace('xx_comment_xx', input_values['comment'])
    return html


#
# For use as client on the robot
#

def connect2wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(settings.wifi_ssid, settings.wifi_password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


class Server:
    def __init__(self):
        self.break_character = settings.break_character
        self.buffer = 1024
        self.skt = socket.socket()
        self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.skt.bind(('', settings.port_number))
        self.skt.listen(1)
        red.on()
        connection, address = self.skt.accept()
        red.off()
        self.connection = connection
        self.address = address
        
    def disconnect(self):
        self.connection.close()
        
    
    def receive_data(self):
        data = ''
        while 1:
            packet = self.connection.recv(self.buffer)
            packet = packet.decode()
            #if not packet: break
            data += packet
            if data.endswith(self.break_character): break
        data = data.rstrip(self.break_character + '\n')
        return data
    
    def send_data(self, message):
        if not message.endswith(self.break_character): message = message +  self.break_character
        encoded_message = message.encode()
        self.connection.sendall(encoded_message)