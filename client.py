import socket, datetime, time
import random, string, sys


def hexlify(s):
    return s.encode().hex()


# key = hexlify(''.join([random.choice(string.ascii_letters) for _ in range(1)]))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('\nconnecting to %s port %s' % server_address)
sock.connect(server_address)
msg = ''
try:
    #     key = hexlify(pesan+' '+str(count))
    while msg != 'end':
        msg = input("Kirim pesan: ")

        if msg != '':
            key = hexlify(msg)
            print('\n', key)
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            sock.sendall(key.encode())

#         count+=1
#         time.sleep(3)

finally:
    print('closing socket')
    sock.close()