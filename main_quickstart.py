#!/usr/bin/python
# -*- encoding: utf-8 -*-

import Tkinter as Tk
import database as db

#Quick start window
class QuickStartWindow(Tk.Toplevel):
    def __init__(self, root):
        #Keep variable target to root
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
        Tk.Button(self, text="Add account", height=4).pack(fill="x")

#Quick start window : account widget for account collector
class QuickStartAccountWidget(Tk.Frame):
    def __init__(self, root, data):
        #Keep variable target to root
        self.root = root

        #Seperate the data
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