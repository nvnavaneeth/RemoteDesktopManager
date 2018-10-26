from main_server_client import *
from remote_desktop_client import *
from ui_windows import *
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

class MainApp:
  def __init__(self, main_server_addr):
    self.main_server_client = MainServerClient(main_server_addr)
    self.rd_client= RemoteDesktopClient()
    self.login_window = LoginWindow()

    self.login_window.verify_desktop_id_cb = self.verify_desktop_id
    self.login_window.verify_password_cb = self.verify_password

    self.login_window.show_all()


  def start(self):
    gtk.main()


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
    return self.rd_client.verify_password(password)

  

if __name__ == "__main__":
    
  host = ''
  port = port = int(sys.argv[1])
  main_server_addr = [host, port]
  MainApp(main_server_addr).start()

