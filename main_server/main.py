import pickle
import socket
import sys
import uuid
from client_service_thread import *
from _thread import *

class Server:
  def __init__(self, host, port):
    self.host = host;
    self.port = port;
    self.create_socket();
    self.next_desktop_id = 123
    # Dict to store whether a remote desktop is ready to receive
    # connections. 
    self.is_ready = {}
    # Dict to store destop_id to remote desktop server address.
    self.remote_desktop_server = {}


  def create_socket(self):
    # Create a socket that uses TCP/IPv4.
    self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.soc.bind((self.host, self.port))


  def run(self):
    self.soc.listen(5)
    while True:
      conn, address = self.soc.accept()

      print("Obtained connection from: ", address[0] + ":" + str(address[1]))
      # Start a new thread to provide service to this client.
      ClientServiceThread(self, conn, address).start()

    self.soc.close()

#----------------------------- MAIN -----------------------------------

host = ''
port = int(sys.argv[1])
server = Server(host, port)

server.run()
