import socket
import pickle

class RemoteDesktopClient:

  def connect(self, address):
    self.soc = socket.socket()
    self.remote_ip, self.remote_port = address
    try:
      self.soc.connect((self.remote_ip, self.remote_port))
    except Exception as e:
      print(e)


  def verify_password(self, password):
    message = ["password", password]
    self.soc.send(pickle.dumps(message))

    reply = pickle.loads(self.soc.recv(1024))

    if reply[0] == "error":
      print(reply[1])
      return False

    elif reply[0] == "authenticated":
      return True

  def send_event(self, event):
    message = ["event", event]
    self.soc.send(pickle.dumps(message))
     

  def close(self):
    print("Terminating connection")
    message = pickle.dumps(["status", "exit"])
    self.soc.send(message)
    self.soc.close() 

