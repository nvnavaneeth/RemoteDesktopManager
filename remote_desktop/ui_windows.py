import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MainWindow(QWidget):
  
  def __init__(self, desktop_id, password):
    super(MainWindow, self).__init__()
    
    self.n_connections = 0

    self.setWindowTitle("Remote Desktop Manager")
    self.create_home_page(desktop_id, password)
    self.resize(300, 150)


  def create_home_page(self, desktop_id, password):
    label_desktop_id = QLabel("Desktop Id")
    label_desktop_id_val = QLabel(":  " + str(desktop_id))
    label_password = QLabel("Password")
    label_password_val = QLabel(":  " + password)
    label_n_connections = QLabel("No of connections")
    self.label_n_connections_val = QLabel(":  " +\
        str(self.n_connections))

    grid = QGridLayout(self)
    grid.setHorizontalSpacing(15)
    grid.addWidget(label_desktop_id, 1, 1)
    grid.addWidget(label_desktop_id_val, 1, 2)
    grid.addWidget(label_password, 2, 1)
    grid.addWidget(label_password_val, 2, 2)
    grid.addWidget(label_n_connections, 3, 1)
    grid.addWidget(self.label_n_connections_val, 3,2)

  def update_connections(self, increment):
    self.n_connections = self.n_connections + increment
    self.label_n_connections_val.setText(str(self.n_connections))

  def screen_grab(self):
    pix = QPixmap.grabWindow(QApplication.desktop( ).winId( ))
    return pix.toImage()
    

if __name__ == "__main__":
  app = QApplication(sys.argv)
  main_window = MainWindow(123, "qwe")

  sys.exit(app.exec_())
