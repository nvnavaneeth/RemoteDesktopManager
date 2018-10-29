from Xlib import X
from Xlib.display import Display
from Xlib.ext.xtest import fake_input


class FakeInputs:
  
  def __init__(self):
    self.display = Display()


  def press_mouse(self, button ,x, y):
    pass

  def release_mouse(self, button, x, y):
    pass

  def move_mouse(self, x, y):
    fake_input(self.display, X.MotionNotify, x=x, y=y)
    self.display.sync()

  def press_key(self, key):
    keycode = self.display.keysym_to_keycode(key)
    fake_input(self.window(), X.KeyPress, keycode)
    self.display.sync()

  def release_key(self, key):
    keycode = self.display.keysym_to_keycode(key)
    fake_input(self.window(), X.KeyRelease, keycode)
    self.display.sync( )

  def window(self):
    return self.display.get_input_focus()._data['focus']


if __name__ == "__main__":
  import time
  fakeinputs = FakeInputs()

  for i in range(5):
    fakeinputs.move_mouse(0,0)
    time.sleep(1)
    fakeinputs.move_mouse(500,500)

