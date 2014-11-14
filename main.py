#!/usr/bin/python
# -*- encoding: utf-8 -*-

import Tkinter as Tk
import database as db

class RootApp:
    def __init__(self):
        self.root = Tk.Tk()

        self.button = Tk.Button(self.root)
        self.button.config(
            text = "สร้างผู้ใช้ใหม่",
            command = self.show_newdatabasedialog,
            font = ("Waffle Regular Regular", "12")
        )
        self.button.pack()

        self.root.mainloop()

    def show_newdatabasedialog(self):
        NewDatabaseDialog(self.root)

class AlertDialog(Tk.Toplevel):
    def __init__(self, root, alert_discription, title = None):
        #Keep the root inside
        self.root = root

        #Create alert dialog
        Tk.Toplevel.__init__(self, self.root)
        #If have title, insert it
        if title:
            self.title(title)

        #Overlay and freeze the main window (root window)
        self.transient(self.root)
        self.grab_set()
        #Set focus to created dialog
        self.focus_set()

        #Create label for description
        self.label_alert = Tk.Label(self)
        self.label_alert.config(
            text = alert_discription,
            font = ("Waffle Regular Regular", "14")
        )
        self.label_alert.pack()

        #Create accept button
        self.btn_accept = Tk.Button(self)
        self.btn_accept.config(
            command = self.acceptdialog,
            text = "OK",
            font = ("Waffle Regular Regular", "12")
        )
        self.btn_accept.pack()

        #Bind protocol for accept this dialog
        self.protocol("WM_DELETE_WINDOW", self.acceptdialog)

    def acceptdialog(self):
        #Destroy this dialog from being accept this
        self.destroy()
        #Focus the root 
        self.root.focus_set()
        self.root.grab_set()


class NewDatabaseDialog(Tk.Toplevel):
    def __init__(self, root):
        #Keep the root inside
        self.root = root

        #Create dialog
        Tk.Toplevel.__init__(self, self.root)
        self.title("New Database")

        #Overlay and freeze the main window (root window)
        self.transient(self.root)
        self.grab_set()
        #Set focus to self dialog
        self.focus_set()

        #Create textbox for new user : database name
        self.textbox_databasename = Tk.Entry(self)
        self.textbox_databasename.config(
            width = 30,
            font = ("Waffle Regular Regular", "16")
        )
        self.textbox_databasename.pack()

        #Create button for new user : submit create new database
        self.btn_submitcreate = Tk.Button(self)
        self.btn_submitcreate.config(
            command = self.submitcreate,
            text = "สร้าง",
            font = ("Waffle Regular Regular", "12")
        )
        self.btn_submitcreate.pack()

        #Bind textbox key event for detecting enter key use to submit create
        self.textbox_databasename.bind("<Key>", self.detectenterkey)
        #Set focus to textbox
        self.textbox_databasename.focus_set()

    def submitcreate(self):
        database_name = self.textbox_databasename.get()
        #Check if textbox is empty, alert user to insert data
        if len(database_name.strip()) == 0:
            #Alert them
            alertdialog = AlertDialog(self, "Please insert some text", "Error")
            #Wait for alertdialog
            self.wait_window(alertdialog)
            #Set focus to textbox
            self.textbox_databasename.focus_set()
            #Return it
            return
        #Call the create database function from database module
        #And store the result
        result = db.createdatabase(database_name)
        #If create successfully
        if result[0]:
            #Alert the success
            alertdialog = AlertDialog(self, result[1], "Result")
            #Wait for alertdialog
            self.wait_window(alertdialog)
            #Destroy ths dialog and focus to root window
            self.destroy()
            self.root.focus_set()
        #If failed to create, result the error
        else:
            #Alert the error
            alertdialog = AlertDialog(self, result[1], "Result")
            #Wait for alertdialog
            self.wait_window(alertdialog)
            #Set focus to textbox
            self.textbox_databasename.focus_set()

    def detectenterkey(self, event):
        #If enter key is passed; 13 is enter keycode
        if event.keycode == 13:
            self.submitcreate()

if __name__ == "__main__":
    root = RootApp()