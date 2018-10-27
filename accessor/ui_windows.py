import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MainWindow(QWidget):

  def __init__(self):
    super(MainWindow, self).__init__()
    self.setFocusPolicy(Qt.StrongFocus)
    self.setMouseTracking(True)

    self.resize(300,300)
    self.show()

  def keyPressEvent(self, event):
    event_desc = {"type": "KeyPress", "key": event.key()}
    print("Key pressed: ", event.key())
    self.event_cb(event_desc)

  def keyReleaseEvent(self, event):
    event_desc = {"type": "KeyRelease", "key": event.key()}
    print("Key release: ", event.key())
    self.event_cb(event_desc)

  def mousePressEvent(self, event):
    event_desc = {"type": "MousePress",
                  "button": event.button(),
                  "x": event.pos().x(),
                  "y": event.pos().y()}
    print("Mouse pressed")
    self.event_cb(event_desc)

  def mouseReleaseEvent(self, event):
    event_desc = {"type": "MouseRelease",
                  "button": event.button(),
                  "x": event.pos().x(),
                  "y": event.pos().y()}
    print("Mouse release")
    self.event_cb(event_desc)

  def mouseMoveEvent(self, event):
    event_desc = {"type": "MouseMove",
                  "button": event.button(),
                  "x": event.pos().x(),
                  "y": event.pos().y()}
    self.event_cb(event_desc)


class PopupWindow(QDialog):
  
  def __init__(self, title, message):
    super(QWidget, self).__init__()
    self.setWindowTitle(title)

    label_msg = QLabel(message)
    btn_ok = QPushButton("Ok")
    btn_ok.clicked.connect(self.close)
    
    layout = QVBoxLayout(self)
    layout.addWidget(label_msg)
    layout.addWidget(btn_ok)

    self.resize(self.sizeHint())
    self.exec_()


class LoginWindow(QMainWindow):

  def __init__(self):
    super(LoginWindow, self).__init__()
    self.setWindowTitle("RemoteDesktopManager")
    self.setGeometry(200, 200, 300, 100)
    
    self.stack = QStackedWidget(self)
    self.create_desktop_id_page()
    self.stack.addWidget(self.desktop_id_page)
    self.stack.resize(self.stack.sizeHint())

    self.show()

  def create_desktop_id_page(self):
    self.desktop_id_page = QWidget()
    
    grid = QGridLayout(self.desktop_id_page)
    grid.setHorizontalSpacing(15)

    label_desktop_id = QLabel("Desktop Id")
    self.entry_desktop_id = QLineEdit()
    self.entry_desktop_id.returnPressed.connect(self.on_click_next)
    btn_next = QPushButton("Next")
    btn_next.clicked.connect(self.on_click_next)

    grid.addWidget(label_desktop_id, 1, 1)
    grid.addWidget(self.entry_desktop_id, 1, 2, 1, 2)
    grid.addWidget(btn_next, 2, 2, 1, 1)

    self.desktop_id_page.resize(self.desktop_id_page.sizeHint())


  def create_password_page(self):
    self.password_page = QWidget()

    grid = QGridLayout(self.password_page)
    grid.setHorizontalSpacing(15)

    label_desktop_id = QLabel("Desktop Id")
    label_desktop_id_val = QLabel(str(self.desktop_id))
    label_password = QLabel("Password")
    self.entry_passowrd = QLineEdit()
    self.entry_passowrd.setEchoMode(QLineEdit.Password)
    self.entry_passowrd.returnPressed.connect(self.on_click_login)
    btn_login= QPushButton("Login")
    btn_login.clicked.connect(self.on_click_login)

    grid.addWidget(label_desktop_id, 1, 1)
    grid.addWidget(label_desktop_id_val, 1, 2, 1, 2)
    grid.addWidget(label_password, 2, 1)
    grid.addWidget(self.entry_passowrd, 2, 2, 1, 2)
    grid.addWidget(btn_login, 3, 2, 1, 1)

    self.desktop_id_page.resize(self.desktop_id_page.sizeHint())


  def on_click_next(self):
    self.desktop_id = self.entry_desktop_id.text()

    valid = self.verify_desktop_id_cb(self.desktop_id)
    if not valid:
      PopupWindow("Error", "Invlaid Desktop Id")
      return

    self.create_password_page()
    self.stack.addWidget(self.password_page)
    self.stack.resize(self.stack.sizeHint())
    self.stack.setCurrentIndex(1)


  def on_click_login(self):
    self.password = self.entry_passowrd.text()

    valid = self.verify_password_cb(self.password)
    if not valid:
      PopupWindow("Error", "Incorrect Password")
      return

    self.close()


def dummy_auth(word):
  if word == "123":
    return True
  return False


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = LoginWindow()
  window.verify_desktop_id_cb = dummy_auth
  window.verify_password_cb = dummy_auth

  main_window = MainWindow()
  
  sys.exit(app.exec_())
