#!usr/bin/python
#-*- encoding: utf-8 -*-
#Wad the duck!

import Tkinter as Tk
from modules.quickstartwindow import Quickstartwindow as window_Quickstartwindow
from modules.mainwindow import Mainwindow as window_Mainwindow

class AccountManagementApps(Tk.Tk):
    def __init__(self):
        #Make root tkinter window
        Tk.Tk.__init__(self)

        #Summon the quick start window when the program is open newly
        self.summon_quickstartwindow()

        #Make application continue running
        self.mainloop()

    def summon_quickstartwindow(self):
        """Summon the Quick start window and hide self 
        -> use when the program is open"""
        #Hide root window and icon
        self.withdraw()
        #Summon the quick start window
        self.quickstartwindow = window_Quickstartwindow(self)

    def summon_mainwindow(self, filename):
        """Summon the Main window the work with account
        (make root window to main window for user to work with account)
        """
        #Restore root window and icon
        self.deiconify()
        #Summon the main window inside the root
        self.mainwindow = window_Mainwindow(self, filename)

    def exitrootprogram(self):
        """Exit the program"""
        #Destroy root window and program
        self.destroy()

if __name__ == "__main__":
    AccountManagementApps()
