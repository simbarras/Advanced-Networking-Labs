# TCP socket on IPv4 using TLS
# usage: python3 secure_pmu.py <port> <certificate> <key>
import socket
import ssl
import sys

# Argument check
if len(sys.argv) != 4:
    print('usage: %s <port> <certificate> <key>' % sys.argv[0], flush=True)
    sys.exit(1)
PORT = int(sys.argv[1])
CERTFILE = sys.argv[2]
KEYFILE = sys.argv[3]
PMU_NUMBER = 10

# Create TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', PORT))
sock.listen()
#print(f"Secure PMU listening on port {PORT}", flush=True)

# Wrap socket with SSL
ssl._create_default_https_context = ssl._create_unverified_context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.verify_mode = ssl.CERT_NONE
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

# Accept connections
while True:
    with context.wrap_socket(sock, server_side=True) as ssl_sock:
        conn, addr = ssl_sock.accept()
        if conn.recv(1024) == b"CMD_short:0":
            for i in range(PMU_NUMBER):
                data_str = f"This is PMU data {i}"
                print(data_str, flush=True)
                conn.sendall(data_str.encode())
        else:
            print("Invalid command received.", flush=True)
        conn.close()
        break
