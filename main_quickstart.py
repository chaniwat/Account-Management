#!/usr/bin/python
# -*- encoding: utf-8 -*-

import Tkinter as Tk
import database as db

#Quick start window
class QuickStartWindow(Tk.Toplevel):
    def __init__(self, root):
        #Keep variable reference to root
        self.root = root

        #Create new window (Toplevel)
        Tk.Toplevel.__init__(self, self.root)
        #Set title
        self.title("Account-Management Quick Start")

        #Hide root window (hide window and icon)
        self.root.withdraw()
        #Focus to self
        self.focus_set()
        #Prevent self to resizing
        self.resizable(0, 0)

        #Create frame for account list
        self.accountlistframe = Tk.Frame(self)
        self.accountlistframe.pack()

        #Set dictionary for collect the account
        self.accountcollector = dict()

        #Get account list that created
        db_list = db.listdatabase()

        #Create and add account widget to collector
        for i, data in zip(xrange(len(db_list)), db_list):
            self.accountcollector[i] = QuickStartAccountWidget(self.accountlistframe, data)

        #Create Button for add new account
        Tk.Button(self, text="Add user", height=4, command=self.summon_adduserwindow).pack(fill="x")

    def summon_adduserwindow(self):
        adduserwindow = QuickStart_AddUserWindow(self)
        self.wait_window(adduserwindow)
        self.focus_set()

#Quick start window : account widget for account collector
class QuickStartAccountWidget(Tk.Frame):
    def __init__(self, root, data):
        #Keep variable reference to root
        self.root = root

        #Seperate the dataคค
        self.filename = data[0]
        self.user_name = data[1]
        self.user_surname = data[2]
        self.lasteditdate = data[3]

        #Create frame for account object that show in collector
        Tk.Frame.__init__(self, self.root, relief='sunken')
        self.pack()

        #Create label and button
        Tk.Label(self, text=self.user_name+" "+self.user_surname, width=50, anchor='w').grid(row=0, column=0)
        Tk.Label(self, text=self.lasteditdate, width=50, anchor='w').grid(row=1, column=0)
        Tk.Button(self, text='Button', bg='#FFFFFF').grid(row=0, column=1, rowspan=2, padx=20, pady=20)

#Add User window : Quick start window : user from window for add new user
class QuickStart_AddUserWindow(Tk.Toplevel):
    def __init__(self, root):
        #Keep variable reference to root
        self.root = root

        #Create new top level
        Tk.Toplevel.__init__(self, self.root)
        #Set title
        self.title("Add User")

        #Overlay and freeze the quick start window (root window)
        self.transient(self.root)
        self.grab_set()
        #Set main focus to self
        self.focus_set()

        #Frame Collector for input textbox frame
        self.textbox_frame = dict()
        #Textbox Collector for data
        self.textbox_collector = dict()
        #Label Collector for label of textbox
        self.textbox_label = dict()
        #Data key for add new user
        data_key = ["name", "surname", "nickname", "birthday", "has_pwd", "pwd", "createdate", "money"]

        #Create label and textbox to insert data for add new user
        for key in data_key:
            self.textbox_frame[key] = Tk.Frame(self)
            self.textbox_frame[key].pack()
            self.textbox_label[key] = Tk.Label(self.textbox_frame[key], text=key)
            self.textbox_label[key].pack(side="left")
            self.textbox_collector[key] = Tk.Entry(self.textbox_frame[key])
            self.textbox_collector[key].config(
                width = 30
            )
            self.textbox_collector[key].pack(side="left")

        #Create button for new user : submit add new user
        self.btn_submitcreate = Tk.Button(self)
        self.btn_submitcreate.config(
            text = "Add new user",
            command = lambda: self.submitecreate(self.textbox_collector)
        )
        self.btn_submitcreate.pack()

    def submitecreate(self, userdata):
        #Fetch all data into dict
        data = dict()
        for key in userdata.keys():
            data[key] = userdata[key].get()
        #Sent to database modules to create the file and handle the result
        sentresult = db.createdatabase(data)
        #Print Result
        print sentresult[1]
        #If result is success, close window
        if sentresult[0]:
            self.destroy()