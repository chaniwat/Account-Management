from Tkinter import *

class root:
    def __init__(self, master):
        self.var = IntVar()
        c = Checkbutton(
            master, text="Enable Tab",
            variable=self.var,
            command=self.cb)
        c.pack()

    def cb(self):
        print "variable is", self.var.get()

master = Tk()

root(master)

mainloop()