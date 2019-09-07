import socket
from recordCPU import RecordCPU

# TCP_IP = '10.130.51.14'
TCP_IP = '127.0.0.1' #localhost
TCP_PORT_IOT = 9999
BUFFER_SIZE = 1024
server_address = (TCP_IP, TCP_PORT_IOT)

# connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

CPU = RecordCPU()

while True:
    #wait for server commands/message
    msg = client_socket.recv(1024).decode('utf-8')

    if(msg == 'mine'):
        CPU.is_mining = True
        CPU.record_cpu = True
        CPU.recordCpuUsage('publish')

    elif(msg == 'done'):
        CPU.is_mining = False
        CPU.record_cpu = False