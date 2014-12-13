#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import database as db
import os, time
from mainwindow import FILE_EXTENSION_DATABASE, ROOT_DIRECTORY_PATH, \
                       DATABASE_DIRECTORY_PATH, MONTH_3_STR_TO_INT
from adduserwindow import Addnewuserwindow as window_Addnewuserwindow

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

        #Create an empty frame for list the user
        self.accountlist_frame = Tk.Frame(self)
        self.accountlist_frame.config(
            width = 0,
            height = 0
        )
        self.accountlist_frame.pack()

        #Add user widget into frame that is for the list of user
        self.listcreateduser(self.accountlist_frame)

        #Create Button for adding new user
        Tk.Button(self, text="Add user", width=70, height=4, command=self.summon_addnewuserwindow).pack(fill="x")

        #Bind the "WM_DELETE_WINDOW" for detect that user was closed this window from a hypothetical menu
        self.protocol("WM_DELETE_WINDOW", self.root.exitrootprogram)

    def __repr__(self):
        return "quickstartwindow"

    def listcreateduser(self, parent):
        """List the user that created in database directory and add user 
        widget that make for user to select to work with or delete 
        the user inside parent frame and return the info of each file
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

        #Create an user widget for every each file that contain in database directory
        for row, file in zip(xrange(len(files)), files):
            self.addwidget_singleuser(parent, file)

    def addwidget_singleuser(self, parent, filename):
        """Add user widget"""
        #Get user_info of user
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
            Tk.Button(frame_temp_btn, text=filename, command=lambda filename=filename: self.selectuser(filename)).pack(fill="x", side="left")
            Tk.Button(frame_temp_btn, text="Delete", command=lambda filename=filename: self.deleteuser(filename)).pack(fill="x", side="left")

    def selectuser(self, filename):
        """Select user to work with and send filename to root for summon main window
        and destroy this window
        """
        self.destroy()
        self.root.summon_mainwindow(filename)      

    def deleteuser(self, filename):
        """Delete the select user (delete database file pernamently)"""
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

    def summon_addnewuserwindow(self):
        """Summon the add new user window to create new user"""
        self.wait_window(window_Addnewuserwindow(self))