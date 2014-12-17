#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import tkFont
import database as db
import md5, time
import mainwindow

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
            self.keysorttype = [u"รายได้/เงินที่ได้", u"อาหาร", u"ซื้อของ", u"ดูหนัง", u"ท่องเที่ยว/เดินทาง", u"จ่ายบิล/อื่นๆ"]
            self.recordtypelist = {u"รายได้/เงินที่ได้":"CHANGE_WALLET_INCOME", u"อาหาร":"CHANGE_WALLET_EAT", u"ซื้อของ":"CHANGE_WALLET_BUY", u"ดูหนัง":"CHANGE_WALLET_ENTERTAINMENT", u"ท่องเที่ยว/เดินทาง":"CHANGE_WALLET_TRAVEL", u"จ่ายบิล/อื่นๆ":"CHANGE_WALLET_BILL"}
        elif accounttype == "ACC_BANK":
            self.keysorttype = [u"ฝากเงิน", u"ถอนเงิน", u"โอน(รับ)", u"โอน(จ่าย)", u"จ่ายเงิน"]
            self.recordtypelist = {u"ฝากเงิน":"CHANGE_BANK_DEPOSIT", u"ถอนเงิน":"CHANGE_BANK_WITHDRAW", u"โอน(รับ)":"CHANGE_BANK_TRANSFER_IN", u"โอน(จ่าย)":"CHANGE_BANK_TRANSFER_OUT", u"จ่ายเงิน":"CHANGE_BANK_PAY"}
        elif accounttype == "ACC_POT":
            self.keysorttype = [u"ออมเงิน", u"ถอนเงิน"]
            self.recordtypelist = {u"ออมเงิน":"CHANGE_POT_DEPOSIT", u"ถอนเงิน":"CHANGE_POT_WITHDRAW"}
        self.currenttypeselect = Tk.StringVar(self)
        self.currenttypeselect.set(self.keysorttype[0])

        self.typeselectmenu = apply(Tk.OptionMenu, (self.input_form, self.currenttypeselect) + (tuple(self.keysorttype)))
        self.typeselectmenu.pack()

        #Create label and textbox for desciption of this record
        Tk.Label(self.input_form, text="รายละเอียดรายการ", font=self.customFont).pack()
        self.description = Tk.Entry(self.input_form)
        self.description.pack()
        #Bind return event
        self.description.bind("<Return>", self.createnewrecord)

        #Create lael and textbox for money of this record
        Tk.Label(self.input_form, text="จำนวนเงิน (จำนวนเต็ม)", font=self.customFont).pack()
        self.money = Tk.Entry(self.input_form)
        self.money.pack()
        #Bind return event
        self.money.bind("<Return>", self.createnewrecord)

        #Create empty frame to create some space
        Tk.Frame(self.input_form, height=15).pack()

        #Create Button to submit the from
        confirmbtn = Tk.Button(self.input_form, width=30, height=1, bd=4, text="เพิ่มรายการใหม่", command=self.createnewrecord, font=self.customFont)
        confirmbtn.pack(fill="x")
        confirmbtn.bind("<Return>", self.createnewrecord)

        self.description.focus_set()

        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = ((self.winfo_screenwidth() // 2) - (w // 2))
        y = ((self.winfo_screenheight() // 2) - (h // 2))
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))

    def createnewrecord(self, *arg):
        #Collect data
        data = dict()
        data["type"] = self.recordtypelist[self.currenttypeselect.get()]
        if self.description.get() == "":
            self.wait_window(mainwindow.Alertdialog(self, text="กรุณาใส่ทำอธิบาย"))
            return False
        else:
            data["description"] = self.description.get()
        if self.money.get() == "":
            self.wait_window(mainwindow.Alertdialog(self, text="กรุณาใส่เงิน"))
            return False
        elif not self.money.get().isdigit():
            self.wait_window(mainwindow.Alertdialog(self, text="กรุณาใส่เงินเป็นตัวเลข"))
            return False
        else:
            data["amtmoney"] = self.money.get()

        self.result = self.main.database.addrecordtocurrentaccount(data)

        if self.result:
            self.destroy()