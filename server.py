import os
import socket
import sys
import time
import Settings
import network

def connect2wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(Settings.wifi_ssid, Settings.wifi_password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


class Server:
    def __init__(self):
        self.break_character = Settings.break_character
        self.buffer = 1024
        self.connection = None
        self.address = None
        self.connect()
    
    def connect(self):
        skt = socket.socket()
        skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        skt.bind(('', Settings.port_number))
        skt.listen(1)
        connection, address = skt.accept()
        self.connection = connection
        self.address = address
        
    def disconnect(self):
        self.connection.close()
        
    
    def receive_data(self):
        data = ''
        while 1:
            packet = self.connection.recv(self.buffer)
            packet = packet.decode()
            if not packet: break
            data += packet
            if data.endswith(self.break_character): break
        data = data.rstrip(self.break_character + '\n')
        return data
    
    def send_data(self, message):
        encoded_message = message.encode()
        self.connection.sendall(encoded_message)