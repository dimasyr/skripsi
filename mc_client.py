import socket
import threading
from recordCPU import RecordCPU

if __name__ == '__main__':

    # TCP_IP = '10.130.59.215'
    TCP_IP = '127.0.0.1'  # localhost
    TCP_PORT = 8881
    BUFFER_SIZE = 1024
    server_address = (TCP_IP, TCP_PORT)

    # connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    CPU = RecordCPU()

    while True:
        #wait for server commands/message
        print('waiting for command...')

        msg = client_socket.recv(1024).decode('utf-8')

        if msg == 'mine':
            print('mining...')
            CPU.is_mining = True
            CPU.record_cpu = True
            threading.Thread(target=CPU.recordCpuUsage).start()

            msg = client_socket.recv(1024).decode('utf-8')
            if msg == 'done':
                CPU.is_mining = False
                CPU.record_cpu = False
                print('done mining.')

        # print grafik cpu usage
        elif msg == 'print':
            print('print')
            CPU.printCpuUsage()

        # print panjang list cpu
        elif msg == 'printlencpu':
            print('printlencpu')
            CPU.lenCPU()

        # menyimpan grafik cpu
        elif msg == 'save':
            CPU.printCpuUsage('publish', True)
            CPU.printCpuUsage('search', True)
            print('figures saved')

        # menyimpan ke file biner
        elif msg== 'savedata':
            CPU.saveData()
            print('File saved.')

        # membaca file biner
        elif msg == 'readdata':
            CPU.readData()
            print('Done reading.')