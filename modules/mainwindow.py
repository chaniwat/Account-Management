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
import quickstartwindow as qs

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

        #Keep filename
        self.filename = filename

        #Connect to database file
        self.database = db.database()
        self.database.connectdatabase(filename)

        #Set current account (default account_id is 1 => wallet)
        self.database.set_currentaccountid(1)

        #SETTING GUI --------------------------------------------------------------------------------------
        #Temporary variable to save the reference to root
        self.root = root

        #set minsize
        self.root.minsize(1150, 600)
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

    def deletethisaccount(self):
        """summon the confirm prompt dialog"""
        #get account type first
        accounttype = self.database.get_currentaccounttype()
        if accounttype == "ACC_WALLET":
            self.root.wait_window(Alertdialog(self.root, text="ไม่สามารถลบบัญชีกระเป๋าเงิน"))
            return False
        else:
            actionresult = confirmdeteleaccountprompt(self.root)
            self.root.wait_window(actionresult)
            if actionresult.result:
                result = self.database.deleteaccount(self.database.get_currentaccountid())
                if result:
                    self.refreshdata()
                    self.account_section.pack_forget()
                    self.account_section.destroy()
                    self.account_section = Main_accountsection(self, self.parentaccount_section)

    def deleterecord(self, record_id):
        """delete the record"""
        #get record type first
        recordtype = self.database.get_recordtype(record_id)
        if recordtype == "CHANGE_INITIATE":
            self.root.wait_window(Alertdialog(self.root, text="ไม่สามารถลบรายการเริ่มต้น"))
            return False
        else:
            actionresult = confirmdetelerecordprompt(self.root)
            self.root.wait_window(actionresult)
            if actionresult.result:
                result = self.database.deleterecord(record_id)
                if result:
                    self.refreshdata()

    def deletethisuser(self):
        """prompt the confirm window and Delete the select user if user confirm (delete database file pernamently)"""
        prompt = qs.confirmdeteleuserprompt(self.root)
        self.root.wait_window(prompt)
        if prompt.result:
            #Get user_info of this user
            data = db.getuserinfoaccount(self.filename)[1]
            #check if filename have password
            if data["USER_HAS_PWD"] == "True":
                passprompt = qs.passwordprompt(self.root, data["USER_PWD"])
                self.root.wait_window(passprompt)
                if passprompt.result:
                    #disconnect from current connect database
                    self.database.closedatabase()
                    #delete database
                    result = db.deleteaccount(self.filename)
                    if result[0]:
                        #call reopen program
                        self.root.reopenprogram()
                    else:
                        print result[1]
                else:
                    return False
            else:      
                #disconnect from current connect database
                self.database.closedatabase()
                #delete database
                result = db.deleteaccount(self.filename)
                if result[0]:
                    #call reopen program
                    self.root.reopenprogram()
                else:
                    print result[1]

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
        self.programmenu.add_command(label="ออกจากโปรแกรม", command=lambda: self.exitprogram(), font=self.customFont)
        self.add_cascade(label="โปรแกรม", menu=self.programmenu, font=self.customFont)

        #user menu
        self.usermenu = Tk.Menu(self, tearoff=0)
        self.usermenu.add_command(label="เปลี่ยนผู้ใช้", command=lambda: self.swapuser(), font=self.customFont)
        self.usermenu.add_command(label="ลบผู้ใช้นี้", command=lambda: self.main.deletethisuser(), font=self.customFont)
        self.add_cascade(label="ผู้ใช้", menu=self.usermenu, font=self.customFont)

        #account menu
        self.accountmenu = Tk.Menu(self, tearoff=0)
        self.accountmenu.add_command(label="ดูบัญชีทั้งหมด", command=lambda: self.summon_accountoverall(), font=self.customFont)
        self.accountmenu.add_separator()
        self.accountmenu.add_command(label="เพิ่มบัญชี" ,command=lambda: self.main.newaccount(), font=self.customFont)
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

    def summon_accountoverall(self):
        """summon the overall account window"""
        overallwindow = totalaccountwindow(self.main, self.main.root)
        self.main.root.wait_window(overallwindow)

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

        #account property section
        self.account_property_section = Main_accountpropertysection(self.main, self.leftmain_section_frame)

        #create a frame inside the canvas which will be scrolled with it
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
        self.accountselectmenu.config(width=25, font=self.customFont)
        self.accountselectmenu.pack(padx=10, pady=25, side="left")
        self.accountselectmenuelement = self.accountselectmenu.children["menu"]
        self.accountselectmenuelement.delete(0, 'end')

        for account in self.accountlist:
            self.accountselectmenuelement.add_command(label=account[1], command=lambda account_id=account[0]: self.changedatareport(account_id), font=self.customFont)

        #Create button to edit the current select account
        Tk.Button(self, text="เพิ่มบัญชีใหม่", command=self.main.newaccount, font=self.customFont).pack(padx=5, side="left")

        #Create frame to make a separator
        Tk.Frame(self, width=2, bd=1, relief="sunken").pack(side="left", fill="y", padx=10, pady=10)

        #Create Label for showing current account
        self.accountnamelabel = Tk.Label(self, text=u"บัญชีปัจจุบัน: "+self.main.database.get_currentaccountname(), font=self.customFont)
        self.accountnamelabel.pack(side="left", pady=25)

        #Create button to delete the current select account
        Tk.Button(self, text="ลบบัญชีปัจจุบัน", command=self.main.deletethisaccount, font=self.customFont).pack(padx=5, side="left")

    def changedatareport(self, account_id):
        """Change data to report to select account"""
        self.customFont = tkFont.Font(family="Browallia New", size=15)

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
        Tk.Frame.__init__(self, self.parent, width=250, height=200, relief="groove", bd=2)
        self.pack(fill="both", expand=1)
        self.pack_propagate(0)

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=15)

        #fetch user info data
        userinfodata = self.main.database.get_currentuserinfo()[1]
        #Create key dict translate to local language
        keys_sort = [u"USER_NAME", u"USER_SURNAME", u"USER_NICKNAME", u"USER_BIRTHDAY", u"USER_CREATEDATE", u"USER_LASTEDITDATE"]
        translate_dict = {u"USER_NAME":u"ชื่อ", u"USER_SURNAME":u"นามสกุล", u"USER_NICKNAME":u"ชื่อเล่น", u"USER_BIRTHDAY":u"วันเกิด", u"USER_CREATEDATE":u"ผู้ใช้สร้างวันที่", u"USER_LASTEDITDATE":u"อัพเดทล่าสุด"}

        #Label for title
        Tk.Label(self, text="ข้อมูลผู้ใช้", font=self.customFont).pack(pady=10)

        for key in keys_sort:
            tempframe = Tk.Frame(self)
            tempframe.pack(fill="x")

            #Create label
            Tk.Label(tempframe, text=translate_dict[key]+u" : "+userinfodata[key], font=self.customFont).pack(side="left")

        separator = Tk.Frame(self, height=2, bd=1, relief="sunken")
        separator.pack(fill="x", padx=5, pady=10)

        #Label for title
        Tk.Label(self, text="ข้อมูลบัญชีปัจจุบัน", font=self.customFont).pack(pady=8)

        #fetch current account info
        accountinfodata = self.main.database.get_currentaccountinfo()
        keys_sort = [u"ชื่อบัญชี", u"ประเภทบัญชี", u"อัพเดทล่าสุด", u"จำนวนเงินปัจจุบัน"]
        translate_dict = {u"ACC_WALLET":u"กระเป๋าเงิน", u"ACC_BANK":u"บัญชีธนาคาร", u"ACC_POT":u"กระปุกเงิน"}
        
        for key, data in zip(keys_sort, accountinfodata):
            tempframe = Tk.Frame(self)
            tempframe.pack(fill="x")

            #Create label
            if key == u"ประเภทบัญชี":
                Tk.Label(tempframe, text=key+u" : %s" % translate_dict[data], font=self.customFont).pack(side="left")
            else:
                Tk.Label(tempframe, text=key+u" : %s" % data, font=self.customFont).pack(side="left")

#Data report table section + support class
class Main_datareportsection:
    def __init__(self, main, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Temporary variable to save the reference to mainwindow
        self.main = main

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=15)

        #Translate
        translate_dict_record = {u"CHANGE_WALLET_INCOME":u"รายได้/เงินที่ได้", u"CHANGE_WALLET_EAT":u"อาหาร", u"CHANGE_WALLET_BUY":u"ซื้อของ", u"CHANGE_WALLET_ENTERTAINMENT":u"ดูหนัง", u"CHANGE_WALLET_TRAVEL":u"ท่องเที่ยว/เดินทาง", u"CHANGE_WALLET_BILL":u"จ่ายบิล/อื่นๆ",
                                u"CHANGE_BANK_DEPOSIT":u"ฝากเงิน", u"CHANGE_BANK_WITHDRAW":u"ถอนเงิน", u"CHANGE_BANK_TRANSFER_IN":u"โอน(รับ)", u"CHANGE_BANK_TRANSFER_OUT":u"โอน(จ่าย)", u"CHANGE_BANK_PAY":u"จ่ายเงิน",
                                u"CHANGE_POT_DEPOSIT":u"ออมเงิน", u"CHANGE_POT_WITHDRAW":u"ถอนเงิน", "CHANGE_INITIATE":u"เริ่มต้น"}

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
            Tk.Label(frametemp, text=translate_dict_record[data[1]], width=25, relief="ridge", bg="white", font=self.customFont).pack(side="left", fill="both")
            Tk.Label(frametemp, wraplength=350, justify="left", text=data[2], relief="ridge", bg="white", font=self.customFont).pack(expand=1, side="left", fill="both")
            Tk.Button(frametemp, width=8, text="ลบ", command=lambda change_id=data[4]: self.main.deleterecord(change_id), font=self.customFont).pack(side="right", ipadx=1)
            Tk.Label(frametemp, width=13, text=data[3], relief="ridge", bg="white", font=self.customFont).pack(side="right", fill="both")

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

class confirmdetelerecordprompt(Tk.Toplevel):
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
        Tk.Label(self, text="ต้องการลบรายการนี้หรือไม่?", font=self.customFont).pack()

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

class totalaccountwindow(Tk.Toplevel):
    def __init__(self, main, parent):
        #Temporary variable to save the reference to main
        self.main = main

        #Temporary variable to save the reference to parent
        self.parent = parent

        #tkFont
        self.customFont = tkFont.Font(family="Browallia New", size=15)

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, self.parent)
        #Set title
        self.title("Account Overview")

        #Overlay and freeze the parent
        self.transient(self.parent)
        self.grab_set()
        #Focus to self
        self.focus_set()

        account_list = self.main.database.get_currentuserallaccount()

        translate_dict = {u"ACC_WALLET":u"กระเป๋าเงิน", u"ACC_BANK":u"บัญชีธนาคาร", u"ACC_POT":u"กระปุกเงิน"}

        moneytotal = 0

        for account in account_list:
            frametemp = Tk.Frame(self, relief="ridge", bd=2)
            frametemp.pack(fill="both")
            frameleft = Tk.Frame(frametemp)
            frameleft.pack(side="left")
            Tk.Label(frameleft, anchor="w", text=u"ชื่อบัญชี : "+account[0], width=50, font=self.customFont).pack(fill="x")
            Tk.Label(frameleft, anchor="w", text=u"ประเภทบัญชี : "+translate_dict[account[1]], font=self.customFont).pack(fill="x")
            Tk.Label(frameleft, anchor="w", text=u"วันสุดท้ายที่อัพเดท : "+account[2], font=self.customFont).pack(fill="x")
            Tk.Label(frameleft, anchor="w", text=u"จำนวนเงิยในบัญชี : "+str(account[3]), font=self.customFont).pack(fill="x")
            frameright = Tk.Frame(frametemp)
            frameright.pack(side="right", fill="y")
            Tk.Button(frameright, text="เปิดบัญชี", width=8, command=lambda account_id=account[4]: self.changeaccount(account_id), font=self.customFont).pack(fill="both", expand=1)
            moneytotal += account[3]

        frametemp = Tk.Frame(self, relief="ridge", bd=2)
        frametemp.pack(fill="both")
        Tk.Label(frametemp, text=u"เงินรวมทั้งหมด : "+str(moneytotal), font=self.customFont).pack(padx=8, pady=8)

        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = ((self.winfo_screenwidth() // 2) - (w // 2))
        y = ((self.winfo_screenheight() // 2) - (h // 2))
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))

    def changeaccount(self, account_id):
        """change account to target id and close self window"""
        self.main.database.set_currentaccountid(account_id)
        self.main.account_section.pack_forget()
        self.main.account_section.destroy()
        self.main.account_section = Main_accountsection(self.main, self.main.parentaccount_section)
        self.main.refreshdata()
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

class Alertdialog(Tk.Toplevel):
    def __init__(self, parent, title="alert", text="alert"):
        Tk.Toplevel.__init__(self, parent)

        #Set title
        self.title(title)

        #Overlay and freeze the parent
        self.transient(parent)
        self.grab_set()
        #Focus to self
        self.focus_set()

        Tk.Label(self, text=text).pack()
        confirmbtn = Tk.Button(self, text="ยืนยัน", command=self.destroy)
        confirmbtn.pack()
        confirmbtn.focus_set()
        def destroyself(*arg):
            self.destroy()
        confirmbtn.bind("<Return>", destroyself)
