import socket, sys, time
from multichain import Multichain
import threading

# TCP_IP = '10.60.101.137'

# ip localhost
TCP_IP = '127.0.0.1'
TCP_PORT = 8881
TCP_PORT_IOT = 8882
BUFFER_SIZE = 1024

HEADERSIZE = 7

class McServer:

    def __init__(self):
        self.CLIENTS = []

    # method untuk memulai server dan menunggu koneksi yang masuk
    def startServer(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((TCP_IP, TCP_PORT))
            sock.listen(5)

            while True:
                client_socket, addr = sock.accept()
                print ('\nConnected with ' + addr[0] + ':' + str(addr[1]))

                # register client
                self.CLIENTS.append(client_socket)

                # print total client
                print('jumlah client:', len(self.CLIENTS), '\n')

            sock.close()

        except socket.error as msg:
            print ('Could Not Start Server Thread. Error Code : '+ str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

    # method untuk mengirim perintah ke semua client multichain
    def broadcast(self, msg):
        for sock in self.CLIENTS:
            try :
                sock.send(msg.encode('utf-8'))

            except socket.error:
                sock.close()  # closing the socket connection
                self.CLIENTS.remove(sock)  # removing the socket from the active connections list

if __name__ == '__main__' :
    # create server
    serv = McServer()

    # listening for connections
    threading.Thread(target=serv.startServer).start()

    # connect to chain1
    Chain1 = Multichain('multichainrpc', 'A4VZcuwWrn36bGCZLrJ5dgg1QUw6CTPPq8fu5jZfQPNc', 'localhost', '7190', 'dyr')

    # create tcp/ip socket for iot
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to the port
    server_address = (TCP_IP, TCP_PORT_IOT)

    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(server_address)

    # listen for incoming iot transmission
    sock.listen(1)
    print('menunggu koneksi perangkat IoT')
    client_socket, client_address = sock.accept()
    print(f'berhasil terhubung dengan perangkat IoT {client_address}')

    msg = ''

    # wait for a connection
    try:
        full_msg = ''
        new_msg = True

        while msg != 'end':
            msg = client_socket.recv(4096)
            full_msg += msg.decode('utf-8')

            if full_msg != 'end':
                if new_msg:
                    # print(f'new message length: {msg[:HEADERSIZE]}')
                    # print('msg = ', msg)
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                if len(full_msg)-HEADERSIZE == msglen:
                    # print("full msg rcvd")
                    hex_msg = full_msg[HEADERSIZE:]
                    # print(hex_msg)
                    # print('ukuran pesan:', sys.getsizeof(hex_msg), 'bytes')
                    true_msg = bytes.fromhex(hex_msg).decode('utf-8')
                    # print('pesan asli:', true_msg)

                    if true_msg == 'printlencpu':
                        serv.broadcast('printlencpu')
                        Chain1.CPU.lenCPU()

                    elif true_msg == 'print':
                        serv.broadcast('print')
                        Chain1.CPU.printCpuUsage()

                    elif true_msg == 'prints':
                        Chain1.CPU.printCpuUsage('search')

                    elif true_msg == 'getfinalmean':
                        serv.broadcast('getfinalmean')
                        Chain1.CPU.getFinalMean()

                    elif true_msg == 'save':
                        serv.broadcast('save')
                        Chain1.CPU.printCpuUsage('publish', True)
                        Chain1.CPU.printCpuUsage('search', True)
                        print('figures saved')

                    elif true_msg == 'savedata':
                        serv.broadcast('savedata')
                        Chain1.CPU.saveData()
                        print('File saved.')

                    elif true_msg == 'readdata':
                        serv.broadcast('readdata')
                        Chain1.CPU.readData()
                        print('Done reading.')

                    elif true_msg[:6] == 'search':
                        Chain1.searchItem('stream1',int(true_msg[6:7]))

                    elif true_msg != 'end' and true_msg!= '':
                        print('\ndata hexa:' , hex_msg)
                        print('teks asli:', true_msg)

                        serv.broadcast('mine')

                        proses = Chain1.publishStream('stream1', 'key1', hex_msg)

                        print('\nproses :', proses)

                        # memberi tahu client mining selesai
                        if proses == 'done':
                            serv.broadcast('done')
                            print('broadcast /done')

                    new_msg = True
                    full_msg = ''

            else:
                msg = full_msg

    finally:
        #   Clean up the connection
        client_socket.close()
        print('connection ended')
