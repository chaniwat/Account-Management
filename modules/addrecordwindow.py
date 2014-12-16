#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import tkFont
import database as db
import md5, time

class Addnewrecordwindow(Tk.Toplevel):
    def __init__(self, main, parent, accounttype):
        #Temporary variable to save the reference to main
        self.main = main

        #Temporary variable to save the reference to parent
        self.parent = parent

        #Pre-defined result for none action
        self.result = False

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, parent)
        #Set title
        self.title("Create new record")

        self.customFont = tkFont.Font(family="Browallia New", size=20)

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

        #Create label and selection menu for change type by current account type
        Tk.Label(self.input_form, text="ประเภทรายการ", font=self.customFont).pack()
        if accounttype == "ACC_WALLET":
            self.recordtypelist = []
            self.recordtypelist_name = ("CHANGE_WALLET_INCOME", "CHANGE_WALLET_EAT", "CHANGE_WALLET_BUY", "CHANGE_WALLET_ENTERTAINMENT", "CHANGE_WALLET_TRAVEL", "CHANGE_WALLET_BILL")
        elif accounttype == "ACC_BANK":
            self.recordtypelist = []
            self.recordtypelist_name = ("CHANGE_BANK_DEPOSIT", "CHANGE_BANK_WITHDRAW", "CHANGE_BANK_TRANSFER", "CHANGE_BANK_PAY")
        elif accounttype == "ACC_POT":
            self.recordtypelist = []
            self.recordtypelist_name = ("CHANGE_POT_DEPOSIT", "CHANGE_POT_WITHDRAW")
        self.currenttypeselect = Tk.StringVar(self)
        self.currenttypeselect.set(self.recordtypelist_name[0])

        self.typeselectmenu = apply(Tk.OptionMenu, (self.input_form, self.currenttypeselect) + (self.recordtypelist_name))
        self.typeselectmenu.pack()

        #Create label and textbox for desciption of this record
        Tk.Label(self.input_form, text="รายละเอียดรายการ", font=self.customFont).pack()
        self.description = Tk.Entry(self.input_form)
        self.description.pack()

        #Create lael and textbox for money of this record
        Tk.Label(self.input_form, text="จำนวนเงิน", font=self.customFont).pack()
        self.money = Tk.Entry(self.input_form)
        self.money.pack()

        #Create empty frame to create some space
        Tk.Frame(self.input_form, height=15).pack()

        #Create Button to submit the from
        Tk.Button(self.input_form, width=30, height=1, bd=4, text="สร้างบัญชีใหม่", command=self.createnewrecord, font=self.customFont).pack(fill="x")

        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = ((self.winfo_screenwidth() // 2) - (w // 2))
        y = ((self.winfo_screenheight() // 2) - (h // 2))
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))

    def createnewrecord(self):
        #Collect data
        data = dict()
        data["type"] = self.currenttypeselect.get()
        data["description"] = self.description.get()
        data["amtmoney"] = self.money.get()

        print data

        self.result = self.main.database.addrecordtocurrentaccount(data)

        if self.result:
            self.destroy()