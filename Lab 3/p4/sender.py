# UDP multicast sender
# Usage: python3 sender.py <multicast_group> <port> <sciper>
import socket
import struct
import sys

# Argument check
if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <multicast_group> <port> <sciper>")
    sys.exit(1)
MCAST_GRP = sys.argv[1]
MCAST_PORT = int(sys.argv[2])
SCIPER = sys.argv[3]

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

while True:
    # Get message from console
    message = input("Enter message to send: ")
    full_message = f"{SCIPER}: {message}"
    # Send message to multicast group
    sock.sendto(full_message.encode(), (MCAST_GRP, MCAST_PORT))
    print(f"Sent: {full_message}")
