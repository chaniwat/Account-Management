#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as Tk

class App:
    def __init__(self, master):
        frame = Tk.Frame(master)
        frame.pack()

        self.button = Tk.Button(frame, text="ออก", fg="red", command=frame.quit)
        self.button.pack(side="left")

        self.hi_there = Tk.Button(frame, text="สวัสดี, คุณเก่ง", command=self.say_hi)
        self.hi_there.pack(side="left")

    def say_hi(self):
        print "Hi there, everyone!"

root = Tk.Tk()
app = App(root)

root.mainloop()
root.destroy()