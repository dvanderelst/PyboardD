import os
import socket
import sys
import time
import Settings
import network

def Connect2WIFI():
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
        
    

        

    
    
Connect2WIFI()
s  = Server()
s.receive_data()
s.send_data('dikke tetten = beste tetten')


# 
# 
# 
# 
# class Server:
#     def __init__(self):
#         # some defaults
#         self.break_character = '*'
# 
#         host = socket.gethostname()
#         self.buffer = 1024
#         self.host = host
#         self.log = []
#         self.sockets = []
#         self.print_log('Starting server at ' + host)
#         self.print_log('Server working directory: ' + os.getcwd())
# 
# 
#     def open_socket(self, port_number):
#         self.sockets.append(port_number)
#         skt = socket.socket()
#         skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         skt.bind(('', port_number))
#         skt.listen(1)
#         return skt
# 
#     def receive_data(self, connection):
#         data = ''
#         while 1:
#             packet = connection.recv(self.buffer)
#             packet = packet.decode()
#             if not packet: break
#             data += packet
#             if data.endswith(self.break_character): break
#         data = data.rstrip(self.break_character + '\n')
#         return data
# 
#     def open_connection(self, port_number, bind_function=Misc.default_function):
#         t = threading.Thread(target=self.open_single_connection, args=(port_number, bind_function))
#         t.start()
# 
#     def close_connection(self, port_number):
#         message = 'close' + self.break_character
#         message = message.encode()
#         self.print_log(['Closing', port_number])
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_address = ('', port_number)
#         sock.connect(server_address)
#         sock.sendall(message)
#         sock.close()
# 
#     def shutdown(self):
#         ports = self.sockets
#         self.print_log(['Shutting down Ports'] + ports)
#         if 12345 in ports: ports.remove(12345)
#         for port_number in ports: self.close_connection(port_number)
#         self.close_connection(12345)
#         self.print_log(['Finished shutting down'])
#         self.sockets = []
# 
#     def open_single_connection(self, port_number, bind_function=Misc.default_function):
#         function_name = bind_function.__name__
#         self.print_log(['Opening connection for', function_name, 'on port', port_number])
#         skt = self.open_socket(port_number)
#         while 1:
#             self.print_log(['Listening for', function_name, 'on port', port_number])
#             connection, address = skt.accept()
#             start = time.time()
#             arguments = self.receive_data(connection)
#             arguments = arguments.split(',')
#             if function_name == 'shutdown':
#                 self.shutdown()
#                 break
#             if 'close' in arguments[0]: break
#             results = bind_function(arguments)
#             results = str(results)
#             if not results.endswith(self.break_character): results += self.break_character
#             results = str(results)
#             results = results.encode()
#             connection.sendall(results)
#             connection.close()
#             stop = time.time()
#             delta = round((stop - start) * 1000)
#             self.print_log(['Response time for', function_name, ':', delta, 'ms'])
#         self.print_log(['Closing connection for', function_name, 'on port', port_number])
#         message = 'closed ' + str(port_number) + self.break_character
#         message = message.encode()
#         if 'close' in arguments[0]: connection.sendall(message)
#         connection.close()
#         skt.close()
# 