# UDP client using IPv4 and IPv6
# usage: python3 PDC.py <server> <port>
import socket
import sys
import select

# Args
if len(sys.argv) != 3:
    print('usage: %s <server> <port>' % sys.argv[0], flush=True)
    sys.exit(1)
HOST = sys.argv[1]
PORT = int(sys.argv[2])
command = "RESET:20"
TIMEOUT_S = 1.0

# Resolve one destination per family (IPv4 + IPv6 if available)
targets = {}
for fam, st, pr, cn, sa in socket.getaddrinfo(HOST, PORT, 0, socket.SOCK_DGRAM):
    if fam in (socket.AF_INET, socket.AF_INET6) and fam not in targets:
        targets[fam] = sa

if not targets:
    print("Could not resolve any UDP address for the server.", flush=True)
    sys.exit(2)

# Create one socket per resolved family; don't bind() for a client
sockets = []
for fam, addr in targets.items():
    s = socket.socket(fam, socket.SOCK_DGRAM)
    s.setblocking(False)
    sockets.append((s, addr))

try:
    attempt = 0
    while True:
        attempt += 1
        # Send the command to all resolved addresses (IPv4 and/or IPv6)
        for s, addr in sockets:
            s.sendto(command.encode(), addr)
        print(f"[attempt {attempt}] sent to: {', '.join(str(a) for _, a in sockets)}", flush=True)

        # Wait up to TIMEOUT_S for any reply
        rlist, _, _ = select.select([s for s, _ in sockets], [], [], TIMEOUT_S)
        if not rlist:
            print("timeout: no response — retransmitting…", flush=True)
            continue

        # Read first available reply and exit
        for rs in rlist:
            try:
                data, addr = rs.recvfrom(4096)
            except BlockingIOError:
                continue
            print(f"received from {addr}: {data.decode('utf-8', 'replace')}", flush=True)
            sys.exit(0)
finally:
    for s, _ in sockets:
        s.close()
