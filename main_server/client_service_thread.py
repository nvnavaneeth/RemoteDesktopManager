import pickle
import socket
import threading
import uuid

class ClientServiceThread(threading.Thread):
  
  def __init__(self, parent, conn, conn_address): 
    self.conn = conn
    self.conn_address = conn_address
    self.address_str = conn_address[0] + ":" + str(conn_address[1])
    
    self.parent = parent
    self.desktop_registered = False

    threading.Thread.__init__(self) 

    self.process_requests = True


  def run(self):
    try:
      while self.process_requests:
        message = pickle.loads(self.conn.recv(1024))
        message_type = message[0]

        if (message_type == "status"): 
          self.process_status(message)

        elif (message_type == "register_request"):
          self.process_register_request(message)

        elif (message_type == "connect_request"):
          self.process_connect_request(message)

    except ex:
      print(ex)
      pass
    
    finally:
      # Close the connection.
      self.close_connection()
      print("Closed connection from: ", self.address_str)


  def process_status(self, message):
    data = message[1]
    if (data == "exit"):
      self.process_requests = False

    elif(data == "ready"):
      self.parent.is_ready[self.desktop_id] = True
      # Get the port number on which the server is listening to.
      remote_server_port = message[2]
      self.parent.remote_desktop_server[self.desktop_id] = [self.conn_address[0], remote_server_port] 
    

  def process_register_request(self, message):
    desktop_id = self.generate_desktop_id(self.address_str)
    self.parent.is_ready[desktop_id] = False;

    self.desktop_registered = True
    self.desktop_id = desktop_id

    # Send credentials to client.
    self.conn.send(desktop_id.encode())
    

  def process_connect_request(self, message):
    desktop_id = message[1]
    if (desktop_id in self.parent.remote_desktop_server) and (self.parent.is_ready[desktop_id]):
      status = "valid"
      addr = self.parent.remote_desktop_server[desktop_id] 
    else:
      status = "invalid"
      addr = ""
          
    self.conn.send(pickle.dumps([status, addr]))
    

  def close_connection(self):
    if self.desktop_registered:
      self.parent.remote_desktop_server.pop(self.desktop_id)
      self.parent.is_ready.pop(self.desktop_id)


  def generate_desktop_id(self, address_str):
    # generate desktop_id.
    desktop_id = str(self.parent.next_desktop_id)
    # TODO: Make this operation thread safe.
    self.next_desktop_id = self.parent.next_desktop_id + 1

    return desktop_id
