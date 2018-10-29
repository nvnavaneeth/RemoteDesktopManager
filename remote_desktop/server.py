import pickle
import select
import socket
import threading
import uuid
import errno
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

#---- Some utility methods--------------------------------------------

def generate_password(length):
  password = str(uuid.uuid4())
  password = password.replace("-","").upper()

  return "qwe"
  #return password[:length]

#---------------------------------------------------------------------

class RemoteDesktopServer(QRunnable):

  def __init__(self, desktop_id):
    super(RemoteDesktopServer, self).__init__()

    self.desktop_id = desktop_id
    self.password = generate_password(8)
    self.exit = False

    self.on_connection_event = None
    self.on_close_connection_event = None

    # Create a socket.
    self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.soc.bind(("",0))
    self.ip, self.port = self.soc.getsockname()


  def run(self):
    self.soc.listen(1)
    try:
      while self.exit == False:
        self.conn, address = self.soc.accept()
        self.process_request()
        # TODO: add proper exit flow here.
        break

    except:
      print("Error occured")

    finally:
      self.close()


  def process_request(self):
    try:
      self.authenticated = self.authenticate()
      if not self.authenticated:
        # Exceutes finally block before return.
        return
      
      if self.on_connection_event != None:
        self.on_connection_event()
      self.main_process()

    except Exception as ex:
      print(ex)

    finally:
      self.conn.close()


  def authenticate(self):
    while True:
      message = pickle.loads(self.conn.recv(1024))
      if message[0] == "exit":
        return False

      elif message[0] == "password":
        if message[1] == self.password:
          message = ["authenticated"]
          self.conn.send(pickle.dumps(message))
          return True
        else:
          message = ["error", "Invalid password"]
          self.conn.send(pickle.dumps(message))

  def main_process(self):
    # Send screens in another thread.
    threading.Thread(target = self.screen_sender_process,
         args = ()).start()

    while(True):
      message = pickle.loads(self.conn.recv(1024))
      print("Received: ", message)
      if message[0] == "event":
        self.process_event(message[1])
      elif message[0] == "status":
        self.process_status(message[1])

  def screen_sender_process(self,interval = 2):
    while True:
      self.screen_grab_signal.emit()
      time.sleep(interval)


  def send_screen(self, pix_map):
    message = ["screen", pix_map]
    print("Sending: ", message)
    self.conn.send(pickle.dumps(message))


  def process_event(self, event):
    # print("Event received: ", event["type"])
    pass


  def process_status(self, status):
    print("Status received")


  def close(self):
    if self.authenticated and self.on_close_connection_event != None:
      self.on_close_connection_event()
    print("Server shutting down")
    self.soc.close()
