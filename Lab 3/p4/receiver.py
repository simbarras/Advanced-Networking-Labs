# UDP multicast receiver
# Usage: python3 receiver.py <multicast_group> <port>
import socket
import struct
import sys

# Argument check
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <multicast_group> <port>")
    sys.exit(1)

MCAST_GRP = sys.argv[1]
MCAST_PORT = int(sys.argv[2])

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Allow multiple sockets to use the same PORT number
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# On macOS you often need SO_REUSEPORT too:
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except (AttributeError, OSError):
    pass

# Bind to all interfaces on the given port
sock.bind(("", MCAST_PORT))

# Join the multicast group on all interfaces
mreq = struct.pack("=4s4s",
                   socket.inet_aton(MCAST_GRP),
                   socket.inet_aton("0.0.0.0"))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Listening for multicast messages on {MCAST_GRP}:{MCAST_PORT}")

# Receive loop
try:
    while True:
        data, addr = sock.recvfrom(1024)
        if not data:
            continue
        print(f"{addr}: {data.decode(errors='replace').strip()}")
except KeyboardInterrupt:
    print("\nExiting.")
finally:
    sock.close()