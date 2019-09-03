import socket, sys, datetime
from multichain import Multichain

# connect to chain1
Chain1 = Multichain('multichainrpc', '44hCoTauwmQTSxtvQ9au99QqzjBs6pkPriqayqjYqF6f', 'localhost', '7172', 'chain1')

# create tcp/ip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the port
# server_address = ('192.168.12.26', 10000) # lan
server_address = ('localhost', 10000) # local

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# listen for incoming transmission
sock.listen(1)
print('menunggu koneksi')
client_socket, client_address = sock.accept()
print(f'connection from {client_address}')

# count = 0

msg = ''

# wait for a connection
try:
    while msg != 'end':
        #   receive the data in bytes
        data = client_socket.recv(4096)

        #   convert bytes to hex string
        data_decode = data.decode()

        #   hex to string
        data_asli = bytes.fromhex(data_decode).decode('utf-8')

        if data_asli == 'printlen':
            Chain1.lenCPU()
            print(Chain1.cpu_usage)
        elif data_asli == 'print':
            Chain1.printCpuUsage()
        elif data_asli != 'end' and data_asli != '':
            now = datetime.datetime.now()
            print('waktu =', now.strftime("%Y-%m-%d %H:%M:%S"))
            print('bytes')
            print(data)
            print('string')
            print(data_decode)
            print('teks asli')
            print(data_asli, '\n')
            Chain1.publishStream('stream1', 'key1', data_decode)

            msg = data_asli
        else:
            msg = data_asli
            print(msg)

finally:
    #   Clean up the connection
    client_socket.close()
    print('connection ended')