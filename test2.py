import Tkinter
root = Tkinter.Tk(  )
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
rootsize = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
x = w/2 - rootsize[0]/2
y = h/2 - rootsize[1]/2
root.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))
for r in range(3):
    for c in range(4):
        Tkinter.Label(root, text='R%s/C%s'%(r,c),
            borderwidth=1 ).grid(row=r,column=c)
root.mainloop(  )