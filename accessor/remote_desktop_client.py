import socket
import pickle
import threading
import select

class RemoteDesktopClient:

  def __inti__(self):
    self.screen_received_cb = None

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

  def main_process(self):
    while True:
      message = pickle.loads(self.soc.recv(1024))
      print("Received :", message)
      if message[0] == "screen":
        self.process_screen(message[1])
      elif message[1] == "status":
        self.process_status(message[1])
    
  def send_event(self, event):
    message = ["event", event]
    print("Sending: ", message)
    self.soc.send(pickle.dumps(message))

  def process_status(self, status):
    pass

  def process_screen(self, pix_map):
    if self.screen_received_cb != None:
      self.screen_received_cb(pix_map)
     

  def close(self):
    print("Terminating connection")
    message = pickle.dumps(["status", "exit"])
    self.soc.send(message)
    self.soc.close() 

