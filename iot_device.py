import socket, datetime, time
import random, string, sys

HEADERSIZE = 7

def hexlify(s):
    return s.encode().hex()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.130.51.237', 9999)
print('\nconnecting to %s port %s' % server_address)
sock.connect(server_address)

msg = ''

try:
    # chat mode
    # 'end' untuk mengakhiri
    while msg != 'end':
        msg = input("Kirim pesan: ")

        if msg != '' and msg != 'end':
            try:
                # random msg with number input
                msg = int(msg)
                hex_msg = hexlify(''.join([random.choice(string.ascii_letters) for _ in range(msg)]))
            except ValueError:
                # not random msg
                hex_msg = hexlify(msg)

            hex_msg2 = f'{len(hex_msg):<{HEADERSIZE}}' + hex_msg

            print('ukuran pesan:', sys.getsizeof(hex_msg), 'bytes')
            print('hex msg:',hex_msg,'\n')
            # now = datetime.datetime.now()
            # print(now.strftime("%Y-%m-%d %H:%M:%S"))
            sock.sendall(hex_msg2.encode())
        else:
            sock.sendall(msg.encode())

    # # iot mode
    # while True:
    #     hex_msg = hexlify(''.join([random.choice(string.ascii_letters) for _ in range(1)]))
    #     print(hex_msg,'\n')
    #     now = datetime.datetime.now()
    #     print(now.strftime("%Y-%m-%d %H:%M:%S"))
    #     sock.sendall(hex_msg.encode())
    #     time.sleep(3)

finally:
    print('closing socket')
    sock.close()