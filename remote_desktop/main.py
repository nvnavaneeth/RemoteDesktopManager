import pickle
import socket
import sys
import time
from server import RemoteDesktopServer


class MainServerClient:
  def __init__(self, server_ip, server_port):
    self.server_ip = server_ip
    self.server_port = port
    self.sock = socket.socket()

    self.sock.connect((self.server_ip, self.server_port))

  def register(self):
    message = pickle.dumps(["register_request"])
    self.sock.send(message)

    # Once registered, server sends a desktop_id.
    self.desktop_id = self.sock.recv(1024).decode()

    return self.desktop_id


  def send_ready(self, port_no):
    message = pickle.dumps(["status", "ready", port_no])
    self.sock.send(message)
   

  def close(self):
    message = pickle.dumps(["status", "exit"])
    self.sock.send(message)

    self.sock.close()

#-------------------MAIN-------------------------

host = ''
port = int(sys.argv[1])
main_server_client = MainServerClient (host, port)

# Register the desktop in main server.
desktop_id = main_server_client.register()

# Create a server to accept incoming connections for remote desktop
# access.
server = RemoteDesktopServer(desktop_id)
server.start()

# Send reaady signal to main server.
main_server_client.send_ready(server.port)
