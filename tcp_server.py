import socket, time, sys
import threading
from multichain import Multichain

TCP_IP = '10.130.51.14'
TCP_PORT = 8888
BUFFER_SIZE = 1024

class server():

    def __init__(self):
        self.CLIENTS = []

    def startServer(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((TCP_IP,TCP_PORT))
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

    def _broadcast(self):        
        for sock in self.CLIENTS:           
            try :
                sock.send(bytes('{"type": "bet","value": "2"}', 'UTF-8'))

            except socket.error:
                sock.close()  # closing the socket connection
                self.CLIENTS.remove(sock)  # removing the socket from the active connections list

if __name__ == '__main__':
    # create new server
    serv = server()

    # listening for connections
    threading.Thread(target=serv.startServer).start()
