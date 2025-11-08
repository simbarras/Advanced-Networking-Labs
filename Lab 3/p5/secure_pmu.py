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
print(f"Secure PMU listening on port {PORT}", flush=True)

# Wrap socket with SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
ssl_sock = context.wrap_socket(sock, server_side=True)

# Accept connections
while True:
    conn, addr = ssl_sock.accept()
    print(f"Connection from {addr}", flush=True)
    try:
        for i in range(PMU_NUMBER):
            print(f"Send PMU {i} data", flush=True)
            conn.sendall(b'This is PMU ' + str(i).encode('utf-8'))
        conn.sendall(b'')
    except Exception as e:
        print(f"Error: {e}", flush=True)
    finally:
        conn.close()
        print(f"Connection from {addr} closed", flush=True)
