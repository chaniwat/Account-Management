#!/usr/bin/python
# -*- encoding: utf-8 -*-

import Tkinter as Tk
import database as db

#import extra window
from main_quickstart import QuickStartWindow

#Main&General window
class RootApp:
    def __init__(self):
        self.root = Tk.Tk()

        #Create Welcome screen
        self.quickstartwindow = QuickStartWindow(self.root)
        #Wait Welcome window to be closed (pause excute code)
        self.root.wait_window(self.quickstartwindow)
        #When Welcome window close, show root window and icon
        self.root.deiconify()

        #Make the application looping
        self.root.mainloop()

if __name__ == "__main__":
    RootApp()