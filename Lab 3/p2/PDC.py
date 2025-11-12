# TCP client
# usage: python3 PDC.py <server> <port> <command>

import socket
import sys
import time
import re

if len(sys.argv) != 4:
    print('usage: %s <server> <port> <command>' % sys.argv[0], flush=True)
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
command = sys.argv[3]

not_connected = True
while not_connected:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        not_connected = False
    except ConnectionRefusedError:
        #print("Connection refused, retrying...", flush=True)
        time.sleep(1)

#print('Connected to server %s:%d' % (HOST, PORT), flush=True)
sock.sendall(command.encode('utf-8'))
#print("sending:", command, flush=True)
count = 1
while True:
    data = sock.recv(1024)
    if not data:
        break
    data_str = data.decode('utf-8')
    #print(f"received ({count}):", data_str, flush=True)
    count += 1
    # insert \n after each number
    formatted_data = re.sub(r'(\d+)', r'\1\n', data_str)
    print(formatted_data)
#print("Closing connection.", flush=True)
sock.close()