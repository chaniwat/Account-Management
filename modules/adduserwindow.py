#!usr/bin/python
#-*- encoding: utf-8 -*-

import Tkinter as Tk
import database as db
import md5, time

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
        self.datakeys = ["name", "surname", "nickname", "birthday", "has_pwd", "pwd", "initmoney"]
        self.datakeys_label = ["ชื่อ", "นามสกุล", "ชื่อเล่น", "วันเกิด (DD-MM-YYYY | ปี ค.ศ.)", "ตั้งรหัสผ่านหรือไม่", "รหัสผ่าน", "เงินปัจจุบัน"]

        #Create label and entry to receive the user input for create new user
        for datakey, label in zip(self.datakeys, self.datakeys_label):
            #Create frame
            frame_temp = Tk.Frame(self.input_form)
            frame_temp.pack()
            #Create Label
            Tk.Label(frame_temp, text=label).pack()
            #Switch by datakey
            if datakey == "has_pwd":
                #Create a variable and checkbox for pwd entry to toggle state
                self.pwdstate = Tk.IntVar()
                self.textboxs[datakey] = Tk.Checkbutton(frame_temp, text="มี", variable=self.pwdstate, command=self.togglepasswordtextbox)
                self.textboxs[datakey].pack()
            elif datakey == "birthday":
                birthframe_temp = Tk.Frame(frame_temp)
                birthframe_temp.pack()
                self.textboxs[datakey+"-d"] = Tk.Entry(birthframe_temp, width=5)
                self.textboxs[datakey+"-d"].pack(side="left")
                Tk.Label(birthframe_temp, text="-").pack(side="left")
                self.textboxs[datakey+"-m"] = Tk.Entry(birthframe_temp, width=5)
                self.textboxs[datakey+"-m"].pack(side="left")
                Tk.Label(birthframe_temp, text="-").pack(side="left")
                self.textboxs[datakey+"-y"] = Tk.Entry(birthframe_temp, width=5)
                self.textboxs[datakey+"-y"].pack(side="left")
            else:
                #Create entry and set variable to reference to this new entry that created
                self.textboxs[datakey] = Tk.Entry(frame_temp)
                self.textboxs[datakey].pack()
                #if datakey is pwd, let it disabled first
                if datakey == "pwd":
                    self.textboxs["pwd"].config(state="disabled")

        #Create Button to submit the from
        Tk.Button(self.input_form, width=80, text="Create new user", command=self.createnewuser, height=3).pack(fill="x")

    def createnewuser(self):
        #Get all data in textbox (entry widget) into dict
        data = dict()
        for key in self.datakeys:
            #if key is has_pwd, do special get
            if key == "has_pwd":
                data[key] = ["False", "True"][self.pwdstate.get()]
            elif key == "birthday":
                data[key] = self.textboxs[key+"-d"].get()+"-"+self.textboxs[key+"-m"].get()+"-"+self.textboxs[key+"-y"].get()
            else:
                #If key is pwd, insert data depend on its state
                if key == "pwd":
                    if self.pwdstate.get():
                        data[key] = self.textboxs[key].get()
                    else:
                        data[key] = "None"
                else:
                    data[key] = self.textboxs[key].get()
        #Get current date and insert into data
        data["createdate"] = time.strftime("%d-%m-%Y")
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

    def togglepasswordtextbox(self):
        """Check if has_pwd is true or not, toggle the disable state of pwd entry"""
        if self.pwdstate.get() == 1:
            self.textboxs["pwd"].config(state="normal")
        else:
            self.textboxs["pwd"].delete(0, Tk.END)
            self.textboxs["pwd"].config(state="disabled")