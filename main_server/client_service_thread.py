import pickle
import socket
import threading
import uuid

class ClientServiceThread(threading.Thread):
  
  def __init__(self, parent, conn, conn_address): 
    self.conn = conn
    self.conn_address = conn_address
    self.parent = parent
    self.desktop_registered = False

    self.address_str = conn_address[0] + ":" + str(conn_address[1])

    threading.Thread.__init__(self) 

  def run(self):

    try:
      while True:
        message = pickle.loads(self.conn.recv(1024))
        message_type = message[0]

        if (message_type == "status"): 
          data = message[1]
          if (data == "exit"):
            break

          elif(data == "ready"):
            self.parent.is_ready[desktop_id] = True
            # Get the port number on which the server is listening to.
            remote_server_port = message[2]
            print(remote_server_port)
            self.parent.remote_desktop_server[desktop_id] = [self.conn_address[0], remote_server_port] 

        elif (message_type == "register_request"):
          desktop_id, password = self.generate_credentials(self.address_str)
          print(self.address_str)
          self.parent.is_ready[desktop_id] = False;

          self.desktop_registered = True

          # Send credentials to client.
          self.conn.send(desktop_id.encode())
          self.conn.send(password.encode())

        elif (message_type == "connect_request"):
          desktop_id = message[1]
          if (desktop_id in self.parent.remote_desktop_server) and (self.parent.is_ready[desktop_id]):
            status = "valid"
            addr = self.parent.remote_desktop_server[desktop_id] 
          else:
            status = "invalid"
            addr = ""
          
          self.conn.send(pickle.dumps([status, addr]))

    except ex:
      print(ex)
      pass
    
    finally:
      # Close the connection.
      if self.desktop_registered:
        self.parent.remote_desktop_server.pop(desktop_id)
        self.parent.passwords.pop(desktop_id)
        self.parent.is_ready.pop(desktop_id)

      print("Closing connection from: ", self.address_str)


  def generate_credentials(self, address_str):
    # generate desktop_id.
    desktop_id = str(self.parent.next_desktop_id)
    # TODO: Make this operation thread safe.
    self.next_desktop_id = self.parent.next_desktop_id + 1

    # Generate password.
    password = str(uuid.uuid4())
    password = password.replace("-","").upper()
    password = password[:8]
    
    # Add both to maps.
    self.parent.desktop_ids[address_str] = desktop_id
    self.parent.passwords[desktop_id] = password

    return desktop_id, password
