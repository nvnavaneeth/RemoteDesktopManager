import pickle
import socket
import threading
import uuid

#---- Some utility methods--------------------------------------------

def generate_password(length):
    password = str(uuid.uuid4())
    password = password.replace("-","").upper()

    return "qwe"
    #return password[:length]


#---------------------------------------------------------------------

class RemoteDesktopServer(threading.Thread):

  def __init__(self, desktop_id):
    self.desktop_id = desktop_id
    self.password = generate_password(8)
    self.exit = False

    # Create a socket.
    self.soc= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.soc.bind(("",0))
    self.ip, self.port = self.soc.getsockname()

    threading.Thread.__init__(self)

    print("Remote desktop server created with desktop Id:", desktop_id)

  def run(self):
    self.soc.listen(1)
    try:
      while self.exit == False:
        conn, address = self.soc.accept()
        self.process_request(conn, address)
        # TODO: add proper exit flow here.
        break

    except:
      print("Error occured")

    finally:
      self.close()


  def process_request(self, conn, address):
    try:
      authenticated = self.authenticate(conn)
      if not authenticated:
        # Exceutes finally block before return.
        return
      
      self.main_process(conn)

    except Exception as ex:
      print(ex)

    finally:
      conn.close()


  def authenticate(self, conn):
    while True:
      message = pickle.loads(conn.recv(1024))
      if message[0] == "exit":
        return False

      elif message[0] == "password":
        if message[1] == self.password:
          message = ["authenticated"]
          conn.send(pickle.dumps(message))
          return True
        else:
          message = ["error", "Invalid password"]
          conn.send(pickle.dumps(message))

  def main_process(self, conn):
    while(True):
      message = pickle.loads(conn.recv(1024))
      if message[0] == "event":
        self.process_event(message[1])
      elif message[0] == "status":
        self.process_status(message[1])


  def process_event(self, event):
    print("Event received: ", event["type"])


  def process_status(self, status):
    print("Status received")


  def close(self):
    print("Server shutting down")
    self.soc.close()
