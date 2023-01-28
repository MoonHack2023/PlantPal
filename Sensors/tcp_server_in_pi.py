import socket
print("We're in tcp server...") # This file should go inside the pi

#select a server port
server_port = 12008
server_name = '' # this should be ip addr of the rasp-pi
#create a TCP socket
welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the server to the localhost at port server_port
welcome_socket.bind((server_name,server_port))

#extra for tcp socket:
welcome_socket.listen(1)

#ready message
print('Server running on port ', server_port , "inside pi")

#Now the loop that actually listens from clients
while True:
    connection_socket, caddr = welcome_socket.accept()
    # cmsg = connection_socket.recv(1024)
    # cmsg.decode()
    # print(cmsg)
    # if cmsg == "b'send'":
    f = open("temphum.txt","r")   # opens temphum.txt inside the pi for reading
# temparray = cmsg.split(";")
# array=[]
    
    line = f.readline()
    array = []
    array.append([line[0],line[1]])
    # print(line)
    connection_socket.send(line.encode()) #sends the data to the TCP client
