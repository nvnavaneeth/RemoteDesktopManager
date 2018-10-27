from main_server_client import *
from remote_desktop_client import *
from ui_windows import *

from PyQt4.QtGui import *
import sys

class MainApp:
  def __init__(self, main_server_addr):
    self.app = QApplication(sys.argv)
    self.main_server_client = MainServerClient(main_server_addr)
    self.rd_client= RemoteDesktopClient()
    self.login_window = LoginWindow()

    self.login_window.verify_desktop_id_cb = self.verify_desktop_id
    self.login_window.verify_password_cb = self.verify_password

    self.authenticated = False


  def start(self):
    self.app.exec_()


  def verify_desktop_id(self, desktop_id):
    status, address  = \
       self.main_server_client.get_desktop_address(desktop_id)
    if status == "invalid":
      return False
    elif status == "valid":
      self.rd_client.connect(address)
      return True

    return False


  def verify_password(self, password):
    authenticated = self.rd_client.verify_password(password)
    if authenticated:
      self.create_main_window()

    return authenticated

  def create_main_window(self):
    self.main_window = MainWindow()
    self.main_window.event_cb = self.rd_client.send_event

  
if __name__ == "__main__":
    
  host = ''
  port = port = int(sys.argv[1])
  main_server_addr = [host, port]
  MainApp(main_server_addr).start()

