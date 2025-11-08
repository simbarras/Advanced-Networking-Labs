# TCP client using websockets
# usage: python3 PDC.py <server> <port> <command>
import websocket
import sys

# Argument check
if len(sys.argv) != 4:
    print('usage: %s <server> <port> <command>' % sys.argv[0])
    sys.exit(1)
HOST = sys.argv[1]
PORT = int(sys.argv[2])
command = sys.argv[3]
url = f"ws://{HOST}:{PORT}"

def on_message(ws, message):
    print("received:", message)

def on_error(ws, error):
    print("error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connected to server %s:%d" % (HOST, PORT))
    print("sending:", command)
    ws.send(command)

ws = websocket.WebSocketApp(url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()


