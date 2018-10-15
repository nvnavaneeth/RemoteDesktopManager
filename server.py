import socket
import sys
import uuid
from _thread import *

class Server:
  def __init__(self, host, port):
    self.host = host;
    self.port = port;
    self.create_socket();
    self.next_desktop_id = 123456
    # Dict to store socket connection to desktop_id mappings.
    self.desktop_ids= {}
    # Dict to store desktop_id to password mappings.
    self.passwords = {}
    # Dict to store whether a remote desktop is ready to receive
    # connections. 
    self.is_ready = {}


  def create_socket(self):
    # Create a socket that uses TCP/IPv4.
    self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.soc.bind((self.host, self.port))


  def client_service_thread(self, conn, address):
    address_str = address[0] + ":" + str(address[1])
    print("Connection from: ", address_str)

    try:
      desktop_id, password = self.generate_credentials(address_str)
      self.is_ready[desktop_id] = False;

      # Send credentials to client.
      conn.send(desktop_id.encode())
      conn.send(password.encode())

      while True:
        data = conn.recv(1024).decode()

        if (data == "exit"):
          break
        
        # Verify the password.
        reply = ""
        if (data == password):
          reply = "valid";
        else:
          reply = "invalid";      
        # Send verification status. 
        conn.sendall(reply.encode())

    except:
      pass
    
    finally:
      # Close the connection.
      desktop_id = self.desktop_ids.pop(address_str)
      if desktop_id:
        self.passwords.pop(desktop_id)
	self.is_ready.pop(desktop_id)

      print("Closing connection from: ", address_str)


  def run(self):
    self.soc.listen(5)
    while True:
      conn, address = self.soc.accept()

      # Start a new thread to provide service to this client.
      start_new_thread(self.client_service_thread, (conn, address))

    self.soc.close()


  def generate_credentials(self, address_str):
    # generate desktop_id.
    desktop_id = str(self.next_desktop_id)
    # TODO: Make this operation thread safe.
    self.next_desktop_id = self.next_desktop_id + 1

    # Generate password.
    password = str(uuid.uuid4())
    password = password.replace("-","").upper()
    password = password[:8]
    
    # Add both to maps.
    self.desktop_ids[address_str] = desktop_id
    self.passwords[desktop_id] = password

    return desktop_id, password


#----------------------------- MAIN -----------------------------------

host = ''
port = int(sys.argv[1])
server = Server(host, port)

server.run()
