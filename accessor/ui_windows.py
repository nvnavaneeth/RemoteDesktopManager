import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk


class PopupWindow(gtk.Window):
  def __init__(self, title, message):
    gtk.Window.__init__(self, title = title)
 
    self.set_border_width(10)
    grid = gtk.Grid(row_spacing = 15)

    label_message = gtk.Label(message)
    button_ok = gtk.Button(label = "Ok")
    button_ok.connect("clicked", self.close)

    grid.attach(label_message, 0, 0, 3, 1)
    grid.attach(button_ok, 1, 1, 1, 1)
    self.add(grid)


  def close(self, widget):
    self.destroy() 


# Dummy authentication functions to use when this is main.
class DummyAuth:
  def verify_desktop_id(self, desktop_id):
    if desktop_id == "123":
      return True
    
    return False

  def verify_password(self, password):
    if password == "qwe":
      return True

    return False
  

class LoginWindow(gtk.Window):
  def __init__(self):
    self.verify_desktop_id_cb= None
    self.verify_password_cb= None

    gtk.Window.__init__(self, title = "Remote Desktop Manager")
    self.set_border_width(10)

    self.stack = gtk.Stack()
    self.stack.set_transition_type(\
        gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
    self.add(self.stack)

    # Page to get desktop Id.
    grid1 = gtk.Grid(row_spacing = 6, column_spacing = 10)

    label_desktop_id = gtk.Label("Desktop Id")
    self.entry_desktop_id = gtk.Entry()
    button_next = gtk.Button(label = "Next")
    button_next.connect("clicked", self.verify_desktop_id)

    grid1.add(label_desktop_id)
    grid1.attach(self.entry_desktop_id, 1, 0, 2, 1)
    grid1.attach(button_next, 1, 1, 1, 1)

    self.stack.add_named(grid1, "desktop_id_page")

    # Page to get password. 
    grid2 = gtk.Grid(row_spacing = 6, column_spacing = 10)

    label_password = gtk.Label("Password")
    self.entry_password = gtk.Entry(visibility = False)    
    button_login = gtk.Button(label = "Login")
    button_login.connect("clicked", self.verify_password)

    grid2.add(label_password)
    grid2.attach(self.entry_password, 1, 0, 2, 1)
    grid2.attach(button_login, 1, 1, 1, 1)

    self.stack.add_named(grid2, "password_page")


  def verify_desktop_id(self, widget):
    desktop_id = self.entry_desktop_id.get_text()
    authenticated = self.verify_desktop_id_cb(desktop_id)
    if authenticated:
      # Show password page.
      self.stack.set_visible_child_full(\
          "password_page", gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
    else:
      PopupWindow("RDM", "Invalid desktop Id").show_all()


  def verify_password(self, widget):
    password = self.entry_password.get_text()
    authenticated = self.verify_password_cb(password)
    if authenticated:
      print("Successfully logged in")
      # TODO: open the main window.
      self.destroy()
    else:
      PopupWindow("RDM", "Error in authenticating").show_all()


if __name__ == "__main__":
  win = LoginWindow()
  dummy_auth = DummyAuth()
  win.verify_desktop_id_cb = dummy_auth.verify_desktop_id
  win.verify_password_cb = dummy_auth.verify_password
  win.connect("destroy", gtk.main_quit)
  win.show_all()
  gtk.main()
