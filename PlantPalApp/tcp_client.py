
# python3 manage.py runserver
# python3 tcp_server.py
# python3 tcp_client.py
# python3 manage.py updatemodels

import socket
import time
print("We're in tcp client...");

#the server name and port client wishes to access
server_name = 'localhost'
server_port = 12008


#send the message to the TCP server
while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))


    #return values from the server
    msg = client_socket.recv(1024)
    print(msg.decode())
    f = open("blog/text_files/temphum.txt", "w")
    f.write(msg.decode())
    time.sleep(20)

