import pickle
import socket
import sys
import time
from server import RemoteDesktopServer
from ui_windows import MainWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def screen_grab():
  pix_map = QPixmap.grabWindow(QApplication.desktop( ).winId( ))
  return pix_map.toImage()


class MainServerClient:
  def __init__(self, server_ip, server_port):
    self.server_ip = server_ip
    self.server_port = server_port
    self.sock = socket.socket()

    self.sock.connect((self.server_ip, self.server_port))

  def register(self):
    message = pickle.dumps(["register_request"])
    self.sock.send(message)

    # Once registered, server sends a desktop_id.
    self.desktop_id = self.sock.recv(1024).decode()

    return self.desktop_id


  def send_ready(self, port_no):
    message = pickle.dumps(["status", "ready", port_no])
    self.sock.send(message)
   

  def close(self):
    message = pickle.dumps(["status", "exit"])
    self.sock.send(message)

    self.sock.close()


class MainApp(QMainWindow):
  take_screenshot = pyqtSignal()

  def __init__(self, args):
    super(MainApp, self).__init__()
    self.main_server_ip = args[1]
    self.main_server_port = int(args[2])

    self.main_server_client = MainServerClient(self.main_server_ip,
        self.main_server_port)
    self.threadpool = QThreadPool()

    self.show()

    desktop_id = self.main_server_client.register()
    self.server = RemoteDesktopServer(desktop_id)

    self.main_window = MainWindow(self.server.desktop_id,
         self.server.password)
    self.main_window.destroyed.connect(self.close) 

    self.setCentralWidget(self.main_window)

    # Funtions to update the no on connections counter in main window.
    self.server.on_connection_event = \
        lambda : self.main_window.update_connections(1)
    self.server.on_close_connection_event = \
        lambda : self.main_window.update_connections(-1)
    self.server.screen_grab_signal = self.take_screenshot

    # Runs server in another thread.
    self.threadpool.start(self.server)
    # Send ready signal to main server.
    self.main_server_client.send_ready(self.server.port)

    self.take_screenshot.connect(self.screen_grab)


  def close(self):
    self.main_server_client.close()
    self.server.close()

  def screen_grab(self):
    print("Grabbing screen")
    pix = QPixmap.grabWindow(QApplication.desktop( ).winId( ))
    self.server.send_screen(pix)

#-------------------MAIN-------------------------
app = QApplication(sys.argv)
main_app = MainApp(sys.argv)
app.exec_()


