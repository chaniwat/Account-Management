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
        self.database.set_currentaccountid(1)

        #Get current account type
        print self.database.get_currentaccounttype()

        #SETTING GUI --------------------------------------------------------------------------------------
        #Temporary variable to save the reference to root
        self.root = root

        #set minsize
        self.root.minsize(800, 500)
        #Set title
        self.root.title("Account-Management")

        #Create menubar
        self.menubar = Main_menubar(self, self.root) 

        #account section
        self.account_section = Main_accountsection(self, self.root)

        #Main section
        self.main_section_frame = Main_mainsection(self, self.root, self.database.get_currentaccountid())
        #END GUI ------------------------------------------------------------------------------------------

        #Bind the "WM_DELETE_WINDOW" for detect that user was closed this window from a hypothetical menu
        self.root.protocol("WM_DELETE_WINDOW", self.closeprogram)

    def refreshdata(self):
        """refresh main section for rebuild new specific data"""
        self.main_section_frame.pack_forget()
        self.main_section_frame.destroy
        self.main_section_frame = Main_mainsection(self, self.root, self.database.get_currentaccountid())

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
        #Program menu
        self.programmenu = Tk.Menu(self, tearoff=0)
        self.programmenu.add_command(label="เปลี่ยนผู้ใช้", command=lambda: self.swapuser())
        self.programmenu.add_command(label="แก้ไขผู้ใช้", command=lambda: hello())
        self.programmenu.add_command(label="ลบผู้ใช้นี้", command=lambda: hello())
        self.programmenu.add_separator()
        self.programmenu.add_command(label="ออกจากโปรแกรม", command=lambda: self.exitprogram())
        self.add_cascade(label="โปรแกรม", menu=self.programmenu)

        #user menu
        self.usermenu = Tk.Menu(self, tearoff=0)
        self.usermenu.add_command(label="สรุปเงินทั้งหมด", command=lambda: hello())
        self.usermenu.add_command(label="ประมาณเงินคงเหลือ", command=lambda: hello())
        self.add_cascade(label="ผู้ใช้", menu=self.usermenu)

        #account menu
        self.accountmenu = Tk.Menu(self, tearoff=0)
        self.accountmenu.add_command(label="แก้ไขบัญชี", command=lambda: hello())
        self.accountmenu.add_command(label="เพิ่มบัญชี" ,command=lambda: hello())
        self.accountmenu.add_command(label="ปิดบัญชี" ,command=lambda: hello())
        self.accountmenu.add_command(label="ลบบัญชี" ,command=lambda: hello())
        self.add_cascade(label="บัญชี", menu=self.accountmenu)

        #Set parent to use this menubar
        self.parent.config(menu=self)

    def swapuser(self):
        """close main window and open the quick start window
        reopen program"""
        #disconnect from current connect database
        self.main.database.closedatabase()
        #call reopen program
        self.main.root.reopenprogram()

    def exitprogram(self):
        """exit the program"""
        self.main.closeprogram()

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
        Tk.Frame.__init__(self, self.parent, bd=2, relief="ridge", padx=15)
        self.pack(fill="x")

        #Create Label for account selection
        Tk.Label(self, text="เลือกบัญชี").pack(side="left", pady=25)

        #Create selection for current account to show
        accounts = list()
        #Unload variable
        for account in self.main.accountlist:
            accounts.append(account[1])
        #Create selection menu
        self.currentaccountselect = Tk.StringVar(self)
        self.currentaccountselect.set(accounts[0])

        self.accountselectmenu = apply(Tk.OptionMenu, (self, self.currentaccountselect) + tuple(accounts))
        self.accountselectmenu.config(width=30)
        self.accountselectmenu.pack(padx=10, pady=25, side="left")

        #Create button to view the current select account
        Tk.Button(self, text="ดูบัญชี", command=self.changedatareport).pack(padx=5, pady=25, side="left")

        #Create frame to make a separator
        Tk.Frame(self, width=2, bd=1, relief="sunken").pack(side="left", fill="y", padx=10, pady=10)

        #Create button to edit the current select account
        Tk.Button(self, text="แกไขบัญชีปัจจุบัน", command=self.editthisaccount).pack(padx=5, side="left")

        #Create button to delete the current select account
        Tk.Button(self, text="ลบบัญชีปัจจุบัน", command=self.deletethisaccount).pack(padx=5, side="left")

    def changedatareport(self):
        """Change data to report to select account"""
        #Find account id
        for account in self.main.accountlist:
            if self.currentaccountselect.get() == account[1]:
                currentaccountselect_id = account[0]
                break
        #Set and refrest data report frame
        self.main.database.set_currentaccountid(currentaccountselect_id)
        self.main.refreshdata()

    def editthisaccount(self):
        pass

    def deletethisaccount(self):
        pass

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
