import socket
import uuid

#---- Some utility methods--------------------------------------------

def generate_password(length):
    password = str(uuid.uuid4())
    password = password.replace("-","").upper()
    return password[:length]


#---------------------------------------------------------------------

class RemoteDesktopServer:
  def __init__(self, desktop_id):
    self.desktop_id = desktop_id
    self.password = generate_password(8)

    # Create a socket.
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind(("",0))
    self.ip, self.port = self.sock.getsockname()

    print("Remote desktop server created")
    
    # Run the server.
    self.run()


  def __del__(self):
    print("Remote desktop server shutting down")


  def get_address(self):
    return self.ip, self.port


  def run(self):
    print("Run method called")
    # TODO: Implement this
