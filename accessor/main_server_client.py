import socket
import pickle

class MainServerClient:
  
  def __init__(self, address):
    self.soc = socket.socket()
    self.soc.connect((address[0], address[1])) 
    print("connected to main server")


  def get_desktop_address(self, desktop_id):
    message = pickle.dumps(["connect_request", desktop_id])
    self.soc.send(message)
    reply = pickle.loads(self.soc.recv(1024))

    return reply

  def close(self):
    message = pickle.dumps(["status", "exit"])
    self.soc.send(message)
    self.soc.close()
    
