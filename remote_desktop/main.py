import pickle
import socket
import sys
from server import RemoteDesktopServer


class MainServerClient:
  def __init__(self, server_ip, server_port):
    self.server_ip = server_ip
    self.server_port = port
    self.sock = socket.socket()


  def run(self):
    self.sock.connect((self.server_ip, self.server_port))

    # Register desktop with main server.
    message = pickle.dumps(["register_request"])
    self.sock.send(message)

    # Once registered, server sends a desktop_id
    # and password.
    self.desktop_id = self.sock.recv(1024).decode()
    self.password = self.sock.recv(1024).decode()
    print(self.desktop_id)

    # Create a server to accept incoming connections for remote desktop
    # access
    self.server = RemoteDesktopServer(self.desktop_id)

    # Send ready status to main server.
    message = pickle.dumps(["status", "ready", self.server.port])
    self.sock.send(message)

    # Exit
    message = pickle.dumps(["status", "exit"])
    self.sock.send(message)

   # while True:
   #    password = input("Enter password\n")

   #    self.sock.send(password.encode())
   #    reply = self.sock.recv(1024).decode()

   #    if reply == "valid":
   #      print("verified")

   #      # Nothing to do, exit.
   #      message = "exit"
   #      self.sock.send(message.encode())
   #      break
   #    else:
   #      print("invalid")

    self.sock.close()

#-------------------MAIN-------------------------

host = ''
port = int(sys.argv[1])
client = MainServerClient (host, port)

client.run()
