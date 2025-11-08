# TCP client
# usage: python3 PDC.py <server> <port> <command>

import socket
import sys
if len(sys.argv) != 4:
    print('usage: %s <server> <port> <command>' % sys.argv[0])
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
command = sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print('Connected to server %s:%d' % (HOST, PORT))
sock.sendall(command.encode('utf-8'))
print("sending:", command)
count = 1
while True:
    data = sock.recv(1024)
    if not data:
        break
    data_str = data.decode('utf-8')
    print(f"received ({count}):", data_str)
    count += 1
print("Closing connection.")
sock.close()