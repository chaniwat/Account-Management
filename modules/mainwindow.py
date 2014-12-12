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
        self.main_section_frame = Main_mainsection(self, self.root)
        #END GUI ------------------------------------------------------------------------------------------

        #BACKEND APPLICATION CODE -------------------------------------------------------------------------
        self.currentaccount = None
        #END APPLICATION CODE -----------------------------------------------------------------------------

    def set_currentaccount(self, wallet="ACC_WALLET"):
        """Set the current account to show to user"""
        self.currentaccount = wallet
        #run a refresh code to rebuild data by using this wallet

    def refresh(self):
        """refresh this frame (self)"""
        self.main_section_frame.pack_forget()
        self.main_section_frame.destroy
        self.main_section_frame = Main_mainsection(self, self.root, "complete")

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
    def __init__(self, main, parent, data="test"):
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

        #account property section
        self.account_property_section = Main_accountpropertysection(self.main, self.leftmain_section_frame)

        #viewtype section
        self.viewtype_section = Main_viewtypesection(self.main, self.leftmain_section_frame)

        #datareport section
        self.datareport_section = Main_datareportsection(self.main, self.rightmain_section_frame, data)

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
        self.refreshbtn = Tk.Button(self, text="refresh", command=lambda: self.main.refresh())
        self.refreshbtn.pack()

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
    def __init__(self, main, parent, data):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #Create label
        self.label1 = Tk.Label(self.parent, text=data)
        self.label1.pack()

#Dedicated window class
class Addnewuserwindow(Tk.Toplevel):
    def __init__(self, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, parent)
        #Set title
        self.title("Create new user")

        #Overlay and freeze the parent
        self.transient(self.parent)
        self.grab_set()
        #Prevent user to resize this window
        self.resizable(0, 0)
        #Focus to self
        self.focus_set()

        #Create a frame for input form
        self.input_form = Tk.Frame(self)
        self.input_form.pack()
        #Create an empty dict variable for keeping the entry widget that used for user to input
        self.textboxs = dict()
        #Data key
        self.datakeys = ["name", "surname", "nickname", "birthday", "has_pwd", "pwd", "createdate", "initmoney"]

        #Create label and entry to receive the user input for create new user
        for datakey in self.datakeys:
            #Create frame
            frame_temp = Tk.Frame(self.input_form)
            frame_temp.pack()
            #Create Label
            Tk.Label(frame_temp, text=datakey).pack()
            #Create entry and set variable to reference to this new entry that created
            self.textboxs[datakey] = Tk.Entry(frame_temp)
            self.textboxs[datakey].pack()

        #Create Button to submit the from
        Tk.Button(self.input_form, width=80, text="Create new user", command=self.createnewuser).pack(fill="x")

    def createnewuser(self):
        #Get all data in textbox (entry widget) into dict
        data = dict()
        for key in self.textboxs.keys():
            data[key] = self.textboxs[key].get()
        #Sent and receive the result to database to create new user
        result = db.createnewaccount(data)
        if result[0]:
            #if parent is quick start window, simply add new user widget to quick start window
            if repr(self.parent) == "quickstartwindow":
                #Refresh the quick start window
                self.parent.refreshthiswindow()
            #Close this window
            self.destroy()
        else:
            print result[1]