import threading
from Tkinter import Tk, ALL
from test2_modules import stage
import tkSnack

root = Tk()
tkSnack.initializeSnack(root)
stage.Stage(root, tkSnack)
root.mainloop()



