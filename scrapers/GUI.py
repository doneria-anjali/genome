from tkinter import *

def callback():
    print(e.get())
    print(e1.get())

master = Tk()
master .minsize(300,300)
master .geometry("620x400")
master .title("Environmental genome")

b = Button(master, text="Let's check", command=callback)
b.place(x=180, y=60)

l = Label(master, text="Enter Zipcode:-")
l.place(x=130, y=0)

l1 = Label(master, text="Enter other info:-")
l1.place(x=130, y=18)

e = Entry(master)
e.place(x=10, y=100)
e.pack()

e1 = Entry(master)
e1.place(x=20, y=150)
e1.pack()

mainloop()
