#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import tkFont
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
        self.minsize(400, 400)

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=20)

        #Create an empty frame for list the user
        self.accountlist_frame = Tk.Frame(self)
        self.accountlist_frame.config(
            width = 0,
            height = 0
        )
        self.accountlist_frame.pack(fill="x")

        #Add user widget into frame that is for the list of user
        self.listcreateduser(self.accountlist_frame)

        #Create Button for adding new user
        Tk.Button(self, text="เพิ่มผู้ใช้ใหม่", bd=4, width=30, height=1, command=self.summon_addnewuserwindow, font=self.customFont).pack(side="bottom", fill="x")

        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))

        #Bind the "WM_DELETE_WINDOW" for detect that user was closed this window from a hypothetical menu
        self.protocol("WM_DELETE_WINDOW", self.root.exitrootprogram)

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
            frame_temp = Tk.Frame(parent, bd=2, pady=10, relief="ridge")
            frame_temp.pack(expand=1, fill="x")
            #Create Label and Button
            Tk.Label(frame_temp, text=data["USER_NAME"]+" "+data["USER_SURNAME"], font=self.customFont).pack()
            frame_temp_btn = Tk.Frame(frame_temp)
            frame_temp_btn.pack()
            Tk.Button(frame_temp_btn, text="Login", command=lambda filename=filename: self.selectuser(filename)).pack(padx=6, side="left")
            Tk.Button(frame_temp_btn, text="Delete", command=lambda filename=filename: self.deleteuser(filename)).pack(padx=6, side="left")

    def selectuser(self, filename):
        """Select user to work with and send filename to root for summon main window
        and destroy this window
        but if select filename has password will prompt the dialog for user to insert password
        """
        #Get user_info of this user
        data = db.getuserinfoaccount(filename)[1]
        #check if filename have password
        if data["USER_HAS_PWD"] == "True":
            passprompt = passwordprompt(self, data["USER_PWD"])
            self.wait_window(passprompt)
            if passprompt.result:
                self.destroy()
                self.root.summon_mainwindow(filename) 
        else:
            self.destroy()
            self.root.summon_mainwindow(filename)              

    def deleteuser(self, filename):
        """prompt the confirm window and Delete the select user if user confirm (delete database file pernamently)"""
        prompt = confirmdeteleuserprompt(self)
        self.wait_window(prompt)
        if prompt.result:
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
        adduserwindow = window_Addnewuserwindow(self)
        self.wait_window(adduserwindow)
        if adduserwindow.result[0]:
            self.selectuser(adduserwindow.result[1])

class passwordprompt(Tk.Toplevel):
    def __init__(self, parent, filepwd):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the vaiue to filepwd
        self.filepwd = filepwd

        #Pre-defined result for none action
        self.result = False

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, parent)
        #Set title
        self.title("Password")

        #Overlay and freeze the parent
        self.transient(self.parent)
        self.grab_set()
        #Window size
        self.minsize(200,100)
        #Focus to self
        self.focus_set()

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=15)
        #Create Label
        Tk.Label(self, text="กรุณาใส่พาสเวริด", font=self.customFont).pack()

        #Create Entry
        self.passwordbox = Tk.Entry(self)
        self.passwordbox.pack()
        self.passwordbox.focus_set()

        #Create action button
        frame_temp = Tk.Frame(self)
        frame_temp.pack()

        Tk.Button(frame_temp, text="ยืนยัน", command=lambda: self.confirmaction(None), font=self.customFont).pack(side="left")
        Tk.Button(frame_temp, text="ยกเลิก", command=self.cancelaction, font=self.customFont).pack(side="left")
        
        #Centered window
        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))

        #bind enter button
        self.passwordbox.bind("<Return>", self.confirmaction)

    def confirmaction(self, event):
        if self.passwordbox.get() == self.filepwd:
            self.result = True
            self.destroy()
        else:
            print "password not match"

    def cancelaction(self):
        self.result = False
        self.destroy()

class confirmdeteleuserprompt(Tk.Toplevel):
    def __init__(self, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Pre-defined result for none action
        self.result = False

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, parent)
        #Set title
        self.title("Confirm")

        #Overlay and freeze the parent
        self.transient(self.parent)
        self.grab_set()
        #Window size
        self.minsize(200,90)
        #Focus to self
        self.focus_set()

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=15)

        #Create Label
        Tk.Label(self, text="ต้องการลบผู้ใช้นี้?", font=self.customFont).pack()

        #Create action button
        frame_temp = Tk.Frame(self)
        frame_temp.pack()

        Tk.Button(frame_temp, text="ยืนยัน", command=self.confirmaction, font=self.customFont).pack(side="left")
        Tk.Button(frame_temp, text="ยกเลิก", command=self.cancelaction, font=self.customFont).pack(side="left")

        #Centered window
        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))


    def confirmaction(self):
        self.result = True
        self.destroy()

    def cancelaction(self):
        self.result = False
        self.destroy()
