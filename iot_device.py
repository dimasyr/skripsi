import socket, time
import random, string, sys

TCP_IP = '10.60.103.30'

# ip localhost
# TCP_IP = '127.0.0.1'

TCP_PORT_IOT = 8882

HEADERSIZE = 7

def hexlify(s):
    return s.encode().hex()



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (TCP_IP, TCP_PORT_IOT)
print('\nconnecting to %s port %s' % server_address)
sock.connect(server_address)

msg = ''

def iotmode(size):
    for i in range(30):
        hex_msg = hexlify(''.join([random.choice(string.ascii_letters) for _ in range(size)]))
        hex_msg2 = f'{len(hex_msg):<{HEADERSIZE}}' + hex_msg

        print('data hexa:', hex_msg, '\n')
        print('ukuran data:', sys.getsizeof(hex_msg), 'bytes')

        sock.sendall(hex_msg2.encode())

        time.sleep(25)
try:
    # chat mode
    # 'end' untuk mengakhiri
    while msg != 'end':
        msg = input("Kirim pesan: ")
        if msg == 'iot32':
            iotmode(4)

        elif msg == 'iot128':
            iotmode(52)

        elif msg != '' and msg != 'end':
            try:
                # random msg with number input
                msg = int(msg)
                hex_msg = hexlify(''.join([random.choice(string.ascii_letters) for _ in range(msg)]))
            except ValueError:
                # not random msg
                hex_msg = hexlify(msg)

            print('ukuran pesan asli:', sys.getsizeof(msg), 'bytes')
            hex_msg2 = f'{len(hex_msg):<{HEADERSIZE}}' + hex_msg
            print('ukuran pesan setelah menjadi hexa:', sys.getsizeof(hex_msg), 'bytes')
            print('hex msg:',hex_msg,'\n')

            sock.sendall(hex_msg2.encode())
        else:
            sock.sendall(msg.encode())

finally:
    print('closing socket')
    sock.close()