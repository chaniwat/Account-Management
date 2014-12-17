#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import tkFont
import database as db
import time
import mainwindow 

class Addnewaccountwindow(Tk.Toplevel):
    def __init__(self, main, parent):
        #Temporary variable to save the reference to main
        self.main = main

        #Temporary variable to save the reference to parent
        self.parent = parent

        #Pre-defined result for none action
        self.result = False

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, parent)
        #Set title
        self.title("Create new account")

        self.customFont = tkFont.Font(family="Browallia New", size=15)

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

        #Label and input textbox for account name
        Tk.Label(self.input_form, text="ชื่อบัญชี (เช่น ธนาคาร A)", font=self.customFont).pack()
        self.namebox = Tk.Entry(self.input_form)
        self.namebox.pack()
        self.namebox.bind("<Return>", self.createnewaccount)

        #Create label and selection menu for account type
        Tk.Label(self.input_form, text="ประเภทของบัญชี", font=self.customFont).pack()
        self.accounttypelist_name = ["บัญชีธนาคาร", "กระปุกเงิน"]
        self.currenttypeselect = Tk.StringVar(self)
        self.currenttypeselect.set(self.accounttypelist_name[0])

        self.typeselectmenu = apply(Tk.OptionMenu, (self.input_form, self.currenttypeselect) + tuple(self.accounttypelist_name))
        self.typeselectmenu.config(width=15, font=self.customFont)
        self.typeselectmenu.pack()
        self.typeselectmenuelement = self.typeselectmenu.children["menu"]
        self.typeselectmenuelement.delete(0, 'end')

        for accounttype in self.accounttypelist_name:
            self.typeselectmenuelement.add_command(label=accounttype, command=lambda accounttype=accounttype: self.currenttypeselect.set(accounttype))

        #Label and input textbox for start money of this account
        Tk.Label(self.input_form, text="เงินเริ่มต้น (จำนวนเต็ม)", font=self.customFont).pack()
        self.moneybox = Tk.Entry(self.input_form)
        self.moneybox.pack()
        self.moneybox.bind("<Return>", self.createnewaccount)

        #Create empty frame to create some space
        Tk.Frame(self.input_form, height=15).pack()

        #Create Button to submit the from
        confirmbtn = Tk.Button(self.input_form, width=30, height=1, bd=4, text="สร้างบัญชีใหม่", command=self.createnewaccount, font=self.customFont)
        confirmbtn.pack(fill="x")
        confirmbtn.bind("<Return>", self.createnewaccount)

        self.namebox.focus_set()

        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = ((self.winfo_screenwidth() // 2) - (w // 2))
        y = ((self.winfo_screenheight() // 2) - (h // 2))
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))

    def createnewaccount(self, *arg):
        #Collect data
        data = dict()
        if self.namebox.get() == "":
            self.wait_window(mainwindow.Alertdialog(self, text="กรุณาใส่ชื่อบัญชี"))
            return False
        else:
            data["name"] = self.namebox.get()
        if self.currenttypeselect.get() == u"บัญชีธนาคาร":
            data["type"] = "ACC_BANK"
        else:
            data["type"] = "ACC_POT"
        if self.moneybox.get() == "":
            self.wait_window(mainwindow.Alertdialog(self, text="กรุณาใส่เงิน"))
            return False
        elif not self.moneybox.get().isdigit():
            self.wait_window(mainwindow.Alertdialog(self, text="กรุณาใส่เงินแค่ตัวเลข"))
            return False
        else:
            data["initmoney"] = self.moneybox.get()

        self.result, self.newid = self.main.database.addaccount(data)

        if self.result:
            self.main.database.set_currentaccountid(self.newid)
            self.destroy()
