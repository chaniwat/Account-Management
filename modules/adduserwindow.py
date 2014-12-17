#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import tkFont
import database as db
import md5, time
from mainwindow import Alertdialog as window_Alertdialog
from validatingentry import MaxLengthEntry

class Addnewuserwindow(Tk.Toplevel):
    def __init__(self, parent):
        #Temporary variable to save the reference to parent
        self.parent = parent

        #Create new window that is the child of parent
        Tk.Toplevel.__init__(self, parent)
        #Set title
        self.title("Create new user")

        self.customFont = tkFont.Font(family="Browallia New", size=20)

        #keep result for none action
        self.result = False, None

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
        self.datakeys = ["name", "surname", "nickname", "birthday", "has_pwd", "pwd", "initmoney"]
        self.datakeys_label = ["ชื่อ", "นามสกุล", "ชื่อเล่น", "วันเกิด (DD-MM-YYYY | ปี ค.ศ.)", "ตั้งรหัสผ่านหรือไม่", "รหัสผ่าน", "เงินปัจจุบัน (เลขจำนวนเต็ม)"]
        self.datakeys_error = {"name":"กรุณากรอกชื่อ", "surname":"กรุณากรอกนามสกุล", "nickname":"กรุณากรอกชื่อเล่น", "initmoney":"กรุณากรอกเงินเริ่มต้น"}

        #Create label and entry to receive the user input for create new user
        for datakey, label in zip(self.datakeys, self.datakeys_label):
            #Create frame
            frame_temp = Tk.Frame(self.input_form)
            frame_temp.pack()
            #Create Label
            Tk.Label(frame_temp, text=label, font=self.customFont).pack()
            #Switch by datakey
            if datakey == "has_pwd":
                #Create a variable and checkbox for pwd entry to toggle state
                self.pwdstate = Tk.IntVar()
                self.textboxs[datakey] = Tk.Checkbutton(frame_temp, text="มี", variable=self.pwdstate, command=self.togglepasswordtextbox, font=self.customFont)
                self.textboxs[datakey].pack()
                #Bind return event
                self.textboxs[datakey].bind("<Return>", self.createnewuser)
            elif datakey == "birthday":
                birthframe_temp = Tk.Frame(frame_temp)
                birthframe_temp.pack()
                self.textboxs[datakey+"-d"] = MaxLengthEntry(birthframe_temp, width=5, maxlength=2)
                self.textboxs[datakey+"-d"].pack(side="left")
                Tk.Label(birthframe_temp, text="-", font=self.customFont).pack(side="left")
                self.textboxs[datakey+"-m"] = MaxLengthEntry(birthframe_temp, width=5, maxlength=2)
                self.textboxs[datakey+"-m"].pack(side="left")
                Tk.Label(birthframe_temp, text="-", font=self.customFont).pack(side="left")
                self.textboxs[datakey+"-y"] = MaxLengthEntry(birthframe_temp, width=5, maxlength=4)
                self.textboxs[datakey+"-y"].pack(side="left")
                #Bind return event
                self.textboxs[datakey+"-d"].bind("<Return>", self.createnewuser)
                self.textboxs[datakey+"-m"].bind("<Return>", self.createnewuser)
                self.textboxs[datakey+"-y"].bind("<Return>", self.createnewuser)
            else:
                #Create entry and set variable to reference to this new entry that created
                self.textboxs[datakey] = Tk.Entry(frame_temp)
                self.textboxs[datakey].pack()
                #if datakey is pwd, let it disabled first
                if datakey == "pwd":
                    self.textboxs["pwd"].config(state="disabled", show="*")
                #Bind return event
                self.textboxs[datakey].bind("<Return>", self.createnewuser)

        #Set focus
        self.textboxs["name"].focus_set()

        #Create empty frame to create some space
        Tk.Frame(self.input_form, height=15).pack()

        #Create Button to submit the from
        confirmbtn = Tk.Button(self.input_form, width=30, height=1, bd=4, text="สร้างผู้ใช้ใหม่", command=lambda: self.createnewuser(None), font=self.customFont)
        confirmbtn.pack(fill="x")
        confirmbtn.bind("<Return>", self.createnewuser)

        self.update()
        w_req, h_req = self.winfo_width(), self.winfo_height()
        w_form = self.winfo_rootx() - self.winfo_x()
        w = w_req + w_form*2
        h = h_req + (self.winfo_rooty() - self.winfo_y()) + w_form
        x = ((self.winfo_screenwidth() // 2) - (w // 2))
        y = ((self.winfo_screenheight() // 2) - (h // 2))
        self.geometry('{0}x{1}+{2}+{3}'.format(w_req, h_req, x, y))

    def createnewuser(self, event):
        #Get all data in textbox (entry widget) into dict
        data = dict()
        for key in self.datakeys:
            #if key is has_pwd, do special get
            if key == "has_pwd":
                data[key] = ["False", "True"][self.pwdstate.get()]
            elif key == "birthday":
                if self.textboxs[key+"-d"].get() == "" or len(self.textboxs[key+"-d"].get()) < 2:
                    self.wait_window(window_Alertdialog(self, text="กรุณากรอกวันเกิดให้ครบ"))
                    self.textboxs[key+"-d"].focus_set()
                    return False
                elif not self.textboxs[key+"-d"].get().isdigit():
                    self.wait_window(window_Alertdialog(self, text="กรุณากรอกวันเกิดเป็นตัวเลข"))
                    self.textboxs[key+"-d"].focus_set()
                    return False
                elif self.textboxs[key+"-m"].get() == "" or len(self.textboxs[key+"-m"].get()) < 2:
                    self.wait_window(window_Alertdialog(self, text="กรุณากรอกเดือนเกิด"))
                    self.textboxs[key+"-m"].focus_set()
                    return False
                elif not self.textboxs[key+"-m"].get().isdigit():
                    self.wait_window(window_Alertdialog(self, text="กรุณากรอกเดือนเกิดเป็นตัวเลข"))
                    self.textboxs[key+"-m"].focus_set()
                    return False
                elif self.textboxs[key+"-y"].get() == "" or len(self.textboxs[key+"-y"].get()) < 4:
                    self.wait_window(window_Alertdialog(self, text="กรุณากรอกปีเกิด"))
                    self.textboxs[key+"-y"].focus_set()
                    return False
                elif not self.textboxs[key+"-y"].get().isdigit():
                    self.wait_window(window_Alertdialog(self, text="กรุณากรอกปีเกิดเป็นตัวเลข"))
                    self.textboxs[key+"-y"].focus_set()
                    return False
                data[key] = self.textboxs[key+"-d"].get()+"-"+self.textboxs[key+"-m"].get()+"-"+self.textboxs[key+"-y"].get()
            else:
                #If key is pwd, insert data depend on its state
                if key == "pwd":
                    if self.pwdstate.get():
                        if self.textboxs[key].get() == "":
                            data[key] = "None"
                        else:
                            data[key] = self.textboxs[key].get()
                    else:
                        data[key] = "None"
                else:
                    if self.textboxs[key].get() == "":
                        self.wait_window(window_Alertdialog(self, text=self.datakeys_error[key]))
                        self.textboxs[key].focus_set()
                        return False
                    elif key == "initmoney" and not self.textboxs[key].get().isdigit():
                        self.wait_window(window_Alertdialog(self, text="เงินใส่เป็นตัวเลขเท่านั้น"))
                        self.textboxs[key].focus_set()
                        return False
                    data[key] = self.textboxs[key].get()
        #Get current date and insert into data
        data["createdate"] = time.strftime("%d-%m-%Y")
        #Sent and receive the result to database to create new user
        result = db.createnewaccount(data)
        if result[0]:
            #Close this window
            self.destroy()
            self.result = True, result[2]
        else:
            if result[1] == "DB_ERR_FILE_EXIST":
                self.wait_window(window_Alertdialog(self, text="ผู้ใช้ซ้ำ"))
            self.result = False, None

    def togglepasswordtextbox(self):
        """Check if has_pwd is true or not, toggle the disable state of pwd entry"""
        if self.pwdstate.get() == 1:
            self.textboxs["pwd"].config(state="normal")
        else:
            self.textboxs["pwd"].delete(0, Tk.END)
            self.textboxs["pwd"].config(state="disabled")