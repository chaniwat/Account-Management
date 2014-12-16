#!usr/bin/python
#-*- encoding: utf-8 -*-

"""
    Core Modules of the program
    Account-Management
    Created by: Meranote, Jirat
"""

import Tkinter as Tk
import tkFont
import database as db
import sys, os, md5, time
from addaccountwindow import Addnewaccountwindow as window_Addnewaccountwindow
from addrecordwindow import Addnewrecordwindow as window_Addnewrecordwindow

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
        print filename

        #Connect to database file
        self.database = db.database()
        self.database.connectdatabase(filename)

        #Set current account (default account_id is 1 => wallet)
        self.database.set_currentaccountid(1)

        #SETTING GUI --------------------------------------------------------------------------------------
        #Temporary variable to save the reference to root
        self.root = root

        #set minsize
        self.root.minsize(1100, 600)
        #Set title
        self.root.title("Account-Management")

        #Create menubar
        self.menubar = Main_menubar(self, self.root)

        #Create parent of account section frame
        self.parentaccount_section = Tk.Frame(self.root)
        self.parentaccount_section.pack(fill="x")

        #account section
        self.account_section = Main_accountsection(self, self.parentaccount_section)

        #Main section
        self.main_section_frame = Main_mainsection(self, self.root, self.database.get_currentaccountid())
        #END GUI ------------------------------------------------------------------------------------------

        #Bind the "WM_DELETE_WINDOW" for detect that user was closed this window from a hypothetical menu
        self.root.protocol("WM_DELETE_WINDOW", self.closeprogram)

    def refreshdata(self):
        """refresh main section for rebuild new specific data"""
        self.main_section_frame.pack_forget()
        self.main_section_frame.destroy()
        self.main_section_frame = Main_mainsection(self, self.root, self.database.get_currentaccountid())

    def closeprogram(self):
        """Close program"""
        self.database.closedatabase()
        self.root.destroy()

    def newaccount(self):
        """summon the add new user window"""
        newaccountwindow = window_Addnewaccountwindow(self, self.root)
        self.root.wait_window(newaccountwindow)
        if newaccountwindow.result:
            self.account_section.pack_forget()
            self.account_section.destroy()
            self.account_section = Main_accountsection(self, self.parentaccount_section)
            self.refreshdata()

    def newrecord(self):
        """summon the add new record window"""
        newrecordwindow = window_Addnewrecordwindow(self, self.root, self.database.get_currentaccounttype())
        self.root.wait_window(newrecordwindow)
        if newrecordwindow.result:
            self.refreshdata()

    def closethisaccount(self):
        print "closethisaccount"

    def deletethisaccount(self):
        """summon the confirm prompt dialog"""
        actionresult = confirmdeteleaccountprompt(self.root)
        self.root.wait_window(actionresult)
        if actionresult.result:
            result = self.database.deleteaccount(self.database.get_currentaccountid())
            if result:
                self.refreshdata()
                self.account_section.pack_forget()
                self.account_section.destroy()
                self.account_section = Main_accountsection(self, self.parentaccount_section)

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

        self.customFont = tkFont.Font(family="Browallia New", size=13)

        #Add menu and submenu
        #Program menu
        self.programmenu = Tk.Menu(self, tearoff=0)
        self.programmenu.add_command(label="เปลี่ยนผู้ใช้", command=lambda: self.swapuser(), font=self.customFont)
        self.programmenu.add_separator()
        self.programmenu.add_command(label="ออกจากโปรแกรม", command=lambda: self.exitprogram(), font=self.customFont)
        self.add_cascade(label="โปรแกรม", menu=self.programmenu, font=self.customFont)

        #user menu
        self.usermenu = Tk.Menu(self, tearoff=0)
        self.usermenu.add_command(label="สรุปเงินทั้งหมด", command=lambda: hello(), font=self.customFont)
        self.usermenu.add_command(label="ประมาณเงินคงเหลือ", command=lambda: hello(), font=self.customFont)
        self.add_cascade(label="ผู้ใช้", menu=self.usermenu, font=self.customFont)

        #account menu
        self.accountmenu = Tk.Menu(self, tearoff=0)
        self.accountmenu.add_command(label="เพิ่มบัญชี" ,command=lambda: self.main.newaccount(), font=self.customFont)
        self.accountmenu.add_command(label="ปิดบัญชี" ,command=lambda: hello(), font=self.customFont)
        self.accountmenu.add_command(label="ลบบัญชี" ,command=lambda: hello(), font=self.customFont)
        self.add_cascade(label="บัญชี", menu=self.accountmenu, font=self.customFont)

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

        self.customFont = tkFont.Font(family="Browallia New", size=13)

        #Get current account type
        print self.main.database.get_currentaccounttype()

        #Create frame
        Tk.Frame.__init__(self, self.parent)
        self.pack(fill="both", expand=1)

        #leftmain section
        self.leftmain_section_frame = Tk.Frame(self)
        self.leftmain_section_frame.pack(side="left", fill="y")

        self.rightsection = Tk.Frame(self)
        self.rightsection.pack(side="left", fill="both", expand=1)

        #Create Button for adding new record
        Tk.Button(self.rightsection, text="เพิ่มรายการ", height=3, command=self.main.newrecord, font=self.customFont).pack(side="top", fill="x")

        #rightmain section
        self.rightmain_section_frame = VerticalScrolledFrame(self.rightsection, relief="groove", bd=3)
        self.rightmain_section_frame.pack(side="bottom", fill="both", expand=1)

        #viewtype section
        self.viewtype_section = Main_viewtypesection(self.main, self.leftmain_section_frame)

        #account property section
        self.account_property_section = Main_accountpropertysection(self.main, self.leftmain_section_frame)

        # create a frame inside the canvas which will be scrolled with it
        self.datareport_section = Main_datareportsection(self.main, self.rightmain_section_frame.interior)

#Account section
class Main_accountsection(Tk.Frame):
    def __init__(self, main, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        self.customFont = tkFont.Font(family="Browallia New", size=15)

        #list the account of this user
        self.accountlist = self.main.database.listaccount()
        if self.accountlist[0]:
            temp = self.accountlist[1]
            self.accountlist = list()
            for account in temp:
                self.accountlist.append((account[0], account[1]))

        #Create frame
        Tk.Frame.__init__(self, self.parent, bd=2, relief="ridge", padx=15)
        self.pack(fill="x")

        #Create Label for account selection
        Tk.Label(self, text="เลือกบัญชี", font=self.customFont).pack(side="left", pady=25)

        #Create selection menu
        self.currentaccountselect = Tk.StringVar(self)
        self.currentaccountselect.set(self.main.database.get_currentaccountname())

        self.accountselectmenu = apply(Tk.OptionMenu, (self, self.currentaccountselect, ''))
        self.accountselectmenu.config(width=25)
        self.accountselectmenu.pack(padx=10, pady=25, side="left")
        self.accountselectmenuelement = self.accountselectmenu.children["menu"]
        self.accountselectmenuelement.delete(0, 'end')

        for account in self.accountlist:
            self.accountselectmenuelement.add_command(label=account[1], command=lambda account_id=account[0]: self.changedatareport(account_id))

        #Create button to edit the current select account
        Tk.Button(self, text="เพิ่มบัญชีใหม่", command=self.main.newaccount, font=self.customFont).pack(padx=5, side="left")

        #Create frame to make a separator
        Tk.Frame(self, width=2, bd=1, relief="sunken").pack(side="left", fill="y", padx=10, pady=10)

        #Create Label for showing current account
        self.accountnamelabel = Tk.Label(self, text=u"บัญชีปัจจุบัน: "+self.main.database.get_currentaccountname(), font=self.customFont)
        self.accountnamelabel.pack(side="left", pady=25)

        #Create button to close the current select account
        Tk.Button(self, text="ปิดบัญชีปัจจุบัน", command=self.main.closethisaccount, font=self.customFont).pack(padx=5, side="left")

        #Create button to delete the current select account
        Tk.Button(self, text="ลบบัญชีปัจจุบัน", command=self.main.deletethisaccount, font=self.customFont).pack(padx=5, side="left")

    def changedatareport(self, account_id):
        """Change data to report to select account"""
        self.customFont = tkFont.Font(family="Browallia New", size=20)

        #Set and refrest data report frame
        self.main.database.set_currentaccountid(account_id)
        self.accountnamelabel.config(text=u"บัญชีปัจจุบัน: "+self.main.database.get_currentaccountname(), font=self.customFont)
        self.currentaccountselect.set(self.main.database.get_currentaccountname())
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
    def __init__(self, main, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=15)

        frametemp = Tk.Frame(self.parent)
        frametemp.pack(fill="x")
        Tk.Label(frametemp, text="วันที่", width=10, relief="ridge", bg="white", font=self.customFont).pack(side="left")
        Tk.Label(frametemp, text="ประเภท", width=25, relief="ridge", bg="white", font=self.customFont).pack(side="left")
        Tk.Label(frametemp, text="คำอธิบาย", relief="ridge", bg="white", font=self.customFont).pack(expand=1, side="left", fill="x")
        Tk.Label(frametemp, text="ลบรายการ", width=9, relief="ridge", bg="white", font=self.customFont).pack(side="right")
        Tk.Label(frametemp, text="จำนวนเงิน", width=13, relief="ridge", bg="white", font=self.customFont).pack(side="right")

        for data in self.main.database.get_currentaccountdataall():
            frametemp = Tk.Frame(self.parent)
            frametemp.pack(fill="x")         
            Tk.Label(frametemp, text=data[0], width=10, relief="ridge", bg="white", font=self.customFont).pack(side="left", fill="both")
            Tk.Label(frametemp, text=data[1], width=25, relief="ridge", bg="white", font=self.customFont).pack(side="left", fill="both")
            Tk.Label(frametemp, wraplength=350, justify="left", text=data[2], relief="ridge", bg="white", font=self.customFont).pack(expand=1, side="left", fill="both")
            Tk.Button(frametemp, width=8, text="ลบ", command=lambda change_id=data[4]: self.printa(change_id), font=self.customFont).pack(side="right", ipadx=1)
            Tk.Label(frametemp, width=13, text=data[3], relief="ridge", bg="white", font=self.customFont).pack(side="right", fill="both")

    def printa(self, text):
        print text

#Dedicated window class
class confirmdeteleaccountprompt(Tk.Toplevel):
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
        self.minsize(200,100)
        #Focus to self
        self.focus_set()

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=15)

        #Create Label
        Tk.Label(self, text="ต้องการลบบัญชีปัจจุบัน?", font=self.customFont).pack()

        #Create action button
        frame_temp = Tk.Frame(self)
        frame_temp.pack()

        Tk.Button(frame_temp, text="ยืนยัน", command=self.confirmaction, font=self.customFont).pack(side="left")
        Tk.Button(frame_temp, text="ยกเลิก", command=self.cancelaction, font=self.customFont).pack(side="left")

        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height(),
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = ((self.winfo_screenwidth() // 2) - (w // 2))
        y = ((self.winfo_screenheight() // 2) - (h // 2))
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))


    def confirmaction(self):
        self.result = True
        self.destroy()

    def cancelaction(self):
        self.result = False
        self.destroy()

#VerticalScrolledFrame
class VerticalScrolledFrame(Tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    
    credit: http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
    """
    def __init__(self, parent, *args, **kw):
        Tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Tk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(fill="y", side="right", expand=0)
        canvas = Tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side="left", fill="both", expand=1)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor="nw")

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(-1*(event.delta/120), "units")

        #Bind mousewheel to scroll
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

   