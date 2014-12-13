#!usr/bin/python
#-*- encoding: utf-8 -*-

"""
    Core Modules of the program
    Account-Management
    Created by: Meranote
"""

import Tkinter as Tk
import database as db
import sys, os, md5, time
from adduserwindow import Addnewuserwindow as window_Addnewuserwindow

#Global Variable use cross the program
#Full directory path that keep core file
CORE_FILE_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))+"\\"
#Backward one step directory to get root path
ROOT_DIRECTORY_PATH = CORE_FILE_DIRECTORY_PATH[:CORE_FILE_DIRECTORY_PATH[:len(CORE_FILE_DIRECTORY_PATH)-1].rindex("\\")]
#Directory name to keep the database file
DATABASE_DIRECTORY_NAME = "accountdata"
#Database file extension
FILE_EXTENSION_DATABASE = ".db"
#Full directory path that keep the database file
DATABASE_DIRECTORY_PATH = ROOT_DIRECTORY_PATH+"\\"+DATABASE_DIRECTORY_NAME+"\\"
#Global month number refer to string
MONTH_3_STR_TO_INT = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9, "SEPT": 9, "OCT": 10, "NOV": 11, "DEC": 12}

#Main window class
class Mainwindow:
    def __init__(self, root, filename):
        #Connect to database file
        self.database = db.database()
        self.database.connectdatabase(filename)

        #list the account of this user
        self.accountlist = self.database.listaccount()
        if self.accountlist[0]:
            temp = self.accountlist[1]
            self.accountlist = list()
            for account in temp:
                self.accountlist.append((account[0], account[1]))

        #Set current account (default account_id is 1 => wallet)
        self.set_currentaccount()

        #SETTING GUI --------------------------------------------------------------------------------------
        #Temporary variable to save the reference to root
        self.root = root

        #set minsize
        self.root.minsize(800, 500)

        #Create menubar
        self.menubar = Main_menubar(self, self.root) 

        #account section
        self.account_section = Main_accountsection(self, self.root)

        #Main section
        self.main_section_frame = Main_mainsection(self, self.root, self.currentaccount)
        #END GUI ------------------------------------------------------------------------------------------

        #Bind the "WM_DELETE_WINDOW" for detect that user was closed this window from a hypothetical menu
        self.root.protocol("WM_DELETE_WINDOW", self.closeprogram)

    def set_currentaccount(self, account_id="1"):
        """Set the current account to show to user"""
        self.currentaccount = account_id
        #run a refresh code to rebuild data by using this wallet

    def refreshdata(self):
        """refresh main section for rebuild new specific data"""
        self.main_section_frame.pack_forget()
        self.main_section_frame.destroy
        self.main_section_frame = Main_mainsection(self, self.root, self.currentaccount)

    def closeprogram(self):
        """Close program"""
        self.database.closedatabase()
        self.root.destroy()

#By Section Class
#Main Menu
class Main_menubar(Tk.Menu):
    def __init__(self, main, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #Create an menu
        Tk.Menu.__init__(self, self.parent)

        #Add menu and submenu
        self.add_command(label="Main", command=self.hello)

        #Set parent to use this menubar
        self.parent.config(menu=self)

    def hello(self):
        print "hello"

#Main Section
class Main_mainsection(Tk.Frame):
    def __init__(self, main, parent, accountdata):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #Create frame
        Tk.Frame.__init__(self, self.parent)
        self.pack(fill="both", expand=1)

        #leftmain section
        self.leftmain_section_frame = Tk.Frame(self)
        self.leftmain_section_frame.pack(side="left", fill="y")

        #rightmain section
        self.rightmain_section_frame = Tk.Frame(self, bg="red")
        self.rightmain_section_frame.pack(side="left", fill="both", expand=1)

        #viewtype section
        self.viewtype_section = Main_viewtypesection(self.main, self.leftmain_section_frame)

        #account property section
        self.account_property_section = Main_accountpropertysection(self.main, self.leftmain_section_frame)

        #datareport section
        self.datareport_section = Main_datareportsection(self.main, self.rightmain_section_frame, accountdata)

#Account section
class Main_accountsection(Tk.Frame):
    def __init__(self, main, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #Create frame
        Tk.Frame.__init__(self, self.parent, height=80, bg="blue")
        self.pack(fill="x")

        #Create button
        self.refreshbtn = Tk.Button(self, text="refresh", command=lambda: self.changedatareport())
        self.refreshbtn.pack()

    def changedatareport(self):
        self.main.set_currentaccount("k")
        self.main.refreshdata()

#Account property section
class Main_accountpropertysection(Tk.Frame):
    def __init__(self, main, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #Create frame
        Tk.Frame.__init__(self, self.parent, width=250, height=200, bg="red")
        self.pack(fill="x")

#View type section
class Main_viewtypesection(Tk.Frame):
    def __init__(self, main, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #Create frame
        Tk.Frame.__init__(self, self.parent, width=250, height=80, bg="orange")
        self.pack(fill="x")

#Data report table section + support class
class Main_datareportsection:
    def __init__(self, main, parent, accountdata):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #Create label
        self.label1 = Tk.Label(self.parent, text=accountdata)
        self.label1.pack()

#Dedicated window class
