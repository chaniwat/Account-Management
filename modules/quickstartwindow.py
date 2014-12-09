#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import database as db
import os, time
from mainwindow import FILE_EXTENSION_DATABASE, ROOT_DIRECTORY_PATH, \
                       DATABASE_DIRECTORY_PATH, MONTH_3_STR_TO_INT
from mainwindow import Addnewaccountwindow as window_Addnewaccountwindow

class Quickstartwindow(Tk.Toplevel):
    def __init__(self, root):
        #Temporary variable to save the reference to root
        self.root = root

        #Create new window that is the child of root
        Tk.Toplevel.__init__(self, root)
        #Set title
        self.title("Account-Management Quick Start")

        #Focus to self
        self.focus_set()
        #Prevent user to resize this window
        self.resizable(0, 0)

        #Create an empty frame for list the account
        self.accountlist_frame = Tk.Frame(self)
        self.accountlist_frame.config(
            width = 0,
            height = 0
        )
        self.accountlist_frame.pack()

        #Add account widget into frame that is for the list of account
        self.listcreatedaccount(self.accountlist_frame)

        #Create Button for adding new account
        Tk.Button(self, text="Add user", width=70, height=4, command=self.summon_addnewaccountwindow).pack(fill="x")

        #Bind the "WM_DELETE_WINDOW" for detect that user was closed this window from a hypothetical menu
        self.protocol("WM_DELETE_WINDOW", self.root.exitrootprogram)

    def __repr__(self):
        return "quickstartwindow"

    def listcreatedaccount(self, parent):
        """List the account that created in database directory and add account 
        widget that make for user to select to work with or delete 
        the account inside parent frame and return the info of each file
        """
        #Check database directory, if not exist not create any widget
        if not os.path.exists(DATABASE_DIRECTORY_PATH):
            return

        #Change working directory to database directory
        os.chdir(DATABASE_DIRECTORY_PATH)

        #List all file that contain in database directory
        files = os.listdir(os.getcwd())
        #Filter only .db files
        files = filter(lambda x: x[-1:-4:-1][::-1] == FILE_EXTENSION_DATABASE, files)

        #Sort file by modify date
        files_key_by_mod_date = list()

        for file in files:
            file_mod_datetime = tuple(time.ctime(os.stat(os.getcwd()+"\\"+file).st_mtime).split())
            file_mod_date = (int(file_mod_datetime[2]), MONTH_3_STR_TO_INT[file_mod_datetime[1].upper()], int(file_mod_datetime[4]))
            files_key_by_mod_date.append((file_mod_date, file))

        files_key_by_mod_date.sort(reverse=True)
        files = list()
        for file_mod_date in files_key_by_mod_date:
            files.append(file_mod_date[1])

        #Create an account widget for every each file that contain in database directory
        for row, file in zip(xrange(len(files)), files):
            self.addwidget_singleaccount(parent, file)

    def addwidget_singleaccount(self, parent, filename):
        """____"""
        #Get user_info of account
        data = db.getuserinfoaccount(filename)
        if data[0]:
            #Convert data tuple to dict
            data = dict(data[1])
            #Create Frame
            frame_temp = Tk.Frame(parent)
            frame_temp.pack()
            #Create Label and Button
            Tk.Label(frame_temp, text=data["USER_NAME"]).pack()
            frame_temp_btn = Tk.Frame(frame_temp)
            frame_temp_btn.pack()
            Tk.Button(frame_temp_btn, text=filename, command=lambda filename=filename: self.selectedaccount(filename)).pack(fill="x", side="left")
            Tk.Button(frame_temp_btn, text="Delete", command=lambda filename=filename: self.deleteaccount(filename)).pack(fill="x", side="left")

    def selectedaccount(self, filename):
        """Select account to work with and send filename to root for summon main window
        and destroy this window
        """
        self.root.summon_mainwindow(filename)
        self.destroy()

    def deleteaccount(self, filename):
        """Delete the select account (delete database file pernamently)"""
        result = db.deleteaccount(filename)
        if result[0]:
            self.refreshthiswindow()
        else:
            print result[1]

    def refreshthiswindow(self):
        """Refresh this window by close and re-summon"""
        import quickstartwindow
        self.destroy()
        quickstartwindow.Quickstartwindow(self.root)

    def summon_addnewaccountwindow(self):
        """Summon the add new user account window to create new account for user"""
        self.wait_window(window_Addnewaccountwindow(self))