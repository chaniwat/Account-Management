import Tkinter as tk

root = tk.Tk()

word = tk.Label(root, text="Hello Tkinter!")
word.pack()

def callback():
    """change text of Label => word"""
    word.config(text="Changed!")

btn_changeword = tk.Button(root, text="Change word", command=callback)
btn_changeword.pack()

tk.mainloop()
