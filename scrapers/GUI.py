from tkinter import Tk, Button, Label, Entry
from tkinter import mainloop
import buildModelAttributes as model

def callback():
    model.buildAll(e.get(), e1.get())
    l2['text'] = "On click display!!"

master = Tk()
master .minsize(300,300)
master .geometry("620x400")
master .title("Environmental genome")

b = Button(master, text="Let's check", command=callback)
b.place(x=220, y=60)

l = Label(master, text="Enter zipcode:")
l.place(x=130, y=0)

l1 = Label(master, text="Enter radius:")
l1.place(x=130, y=18)

l2 = Label(master, text="")
l2.place(x=130, y=36)

e = Entry(master)
e.place(x=10, y=100)
e.pack()

e1 = Entry(master)
e1.place(x=20, y=150)
e1.pack()

mainloop()
