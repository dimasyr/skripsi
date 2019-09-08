import socket
import threading
from recordCPU import RecordCPU

TCP_IP = '10.130.51.237'
# TCP_IP = '127.0.0.1' #localhost
TCP_PORT = 8889
BUFFER_SIZE = 1024
server_address = (TCP_IP, TCP_PORT)

# connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

CPU = RecordCPU()
th = threading.Thread(target=CPU.recordCpuUsage)
while True:
    #wait for server commands/message
    print('waiting for command...')
    msg = client_socket.recv(1024).decode('utf-8')

    if(msg == 'mine'):
        print('mining...')
        CPU.is_mining = True
        CPU.record_cpu = True
        th.start()
        # mining terus dadakno

    elif(msg == 'done'):
        print('done mining.')
        CPU.is_mining = False
        CPU.record_cpu = False

    elif (msg == 'print'):
        print('print')
        CPU.printCpuUsage()

    print('\nnext step\n')