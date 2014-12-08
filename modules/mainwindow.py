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

class Mainwindow:
    def __init__(self):
        pass

#Dedicated window class
class Addnewaccountwindow(Tk.Toplevel):
    def __init__(self, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, parent)
        #Set title
        self.title("Create new user account")

        #Overlay and freeze the parent
        self.transient(self.parent)
        self.grab_set()
        #Focus to self
        self.focus_set()

        #Create a frame for input form
        self.input_form = Tk.Frame(self)
        self.input_form.pack()
        #Create an empty dict variable for keeping the entry widget that used for user to input
        self.textboxs = dict()
        #Data key
        self.datakeys = ["name", "surname", "nickname", "birthday", "has_pwd", "pwd", "createdate", "initmoney"]

        #Create label and entry to receive the user input for create new account
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
        Tk.Button(self.input_form, text="Create new account", command=self.createnewuseraccount).pack(fill="x")

    def createnewuseraccount(self):
        #Get all data in textbox (entry widget) into dict
        data = dict()
        for key in self.textboxs.keys():
            data[key] = self.textboxs[key].get()
        #Sent and receive the result to database to create new user account
        result = db.createnewaccount(data)
        if result[0]:
            #if parent is quick start window, simply add new account widget to quick start window
            if repr(self.parent) == "quickstartwindow":
                #Add account widget inside list
                self.parent.addwidget_singleaccount(self.parent.accountlist_frame, result[2])
            #Close this window
            self.destroy()
        else:
            print result[1]