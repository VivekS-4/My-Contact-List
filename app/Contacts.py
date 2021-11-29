import sqlite3
from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar
from tkinter import ttk, Scrollbar, Toplevel



class Contacts:
    db_file = 'contacts.db'

    def __init__(self, root):
        self.root = root
        self.gui()
        ttk.Style().configure("Treeview.Heading", font="bold")

    def gui(self):
        self.create_LeftIcon()
        self.labelFrame()
        self.msgs()
        self.treeView()
        self.create_scrollbar()
        self.create_BottomButton()

    @staticmethod
    def create_LeftIcon():
        photo = PhotoImage(file='Icon/logo.gif')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=2)

    def labelFrame(self):
        labelframe = LabelFrame(self.root, text="Create new Contact", bg="sky blue")
        labelframe.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        labelframe.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        Label(labelframe, bg="sky blue", text="Name", fg="green").grid(sticky="W", row=1, column=1, padx=15, pady=2)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1, column=2, padx=5, pady=2, sticky="W")
        Label(labelframe, text="Email", bg="sky blue", fg="Brown").grid(row=2, sticky="W", column=1, padx=15, pady=2)
        self.emialfield = Entry(labelframe)
        self.emialfield.grid(row=2, column=2, padx=5, pady=2, sticky="W")
        Label(labelframe, bg="sky blue", text="Number").grid(row=3, column=1, padx=15, pady=2, sticky="W")
        self.numfield = Entry(labelframe)
        self.numfield.grid(row=3, column=2, padx=5, pady=2, sticky="W")
        Button(labelframe, text="Add Contact", command="", bg="white",fg="Blue").grid(row=4, column=2, padx=5, pady=5)

    def msgs(self):
        self.message = Label(text='', fg="red")
        self.message.grid(row=3, column=1, sticky="E")

    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient="vertical", command=self.tree.yview())
        self.scrollbar.grid(row=6, column=3, rowspan=10, sticky='sn')

    def create_BottomButton(self):
        Button().grid(row =8, column=0, padx=50)
        Button(text='Delete Selected', command="", bg='white', fg='red', ).grid(row=8, column=1, sticky=W, padx=10,
                                                                                pady=20)
        Button(text="Modify Selected", command="", bg='white', fg='purple').grid(row=8, column=2, sticky=W)

    def treeView(self):
        self.tree = ttk.Treeview(height=10, columns=("Email", "Phone Number"))
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading("#0", text="Name", anchor=W)
        self.tree.heading("Email", text="Email Address", anchor=W)
        self.tree.heading("Phone Number", text='Contact Number', anchor=W)


# Beginning of GUI
if __name__ == "__main__":
    """Application Designed"""
    root = Tk()
    root.title("My Contact List")
    """Saying the compiler to run every code that is in class"""
    application = Contacts(root)
    root.mainloop()
